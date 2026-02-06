"""
Event clustering using HDBSCAN.
"""
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import numpy as np
import hdbscan

from .embedder import EmbeddedSnippet

logger = logging.getLogger(__name__)


@dataclass
class EventCluster:
    """A cluster of snippets representing a single event."""
    id: str
    snippets: list[EmbeddedSnippet]
    centroid: np.ndarray

    # Computed properties
    sources: set[str] = field(default_factory=set)
    source_types: set[str] = field(default_factory=set)

    def __post_init__(self):
        self.sources = {s.source_name for s in self.snippets}
        self.source_types = {s.source_type for s in self.snippets}

    @property
    def representative_title(self) -> str:
        """Return title closest to centroid."""
        if not self.snippets:
            return ""
        # Find snippet with embedding closest to centroid
        similarities = [
            np.dot(s.embedding, self.centroid) for s in self.snippets
        ]
        best_idx = np.argmax(similarities)
        return self.snippets[best_idx].title

    @property
    def has_wire_coverage(self) -> bool:
        return "wire" in self.source_types

    @property
    def unique_source_count(self) -> int:
        return len(self.sources)


class EventClusterer:
    """
    Clusters snippets into events using HDBSCAN + singleton absorption +
    coherence validation.

    Three-phase approach:
    1. HDBSCAN identifies core multi-article clusters
    2. Singletons are absorbed into nearest cluster if similarity is high
       enough AND the match is clearly better than the second-best option
    3. Clusters with low avg pairwise cosine similarity are dissolved into
       singletons (catches "same-register slop" from e.g. transcript expansion)
    """

    def __init__(
        self,
        min_cluster_size: int = 2,
        min_samples: int = 1,
        cluster_selection_epsilon: float = 0.3,
        absorb_threshold: float = 0.85,
        absorb_min_gap: float = 0.03,
        # Relaxed absorption for clear winners
        absorb_threshold_relaxed: float = 0.80,
        absorb_min_gap_relaxed: float = 0.20,
        min_cluster_coherence: float = 0.55,
        max_cluster_size: int = 8,
        # Source overlap threshold for re-merging sub-clusters
        source_overlap_merge_threshold: int = 3,
    ):
        self.min_cluster_size = min_cluster_size
        self.min_samples = min_samples
        self.cluster_selection_epsilon = cluster_selection_epsilon
        self.absorb_threshold = absorb_threshold
        self.absorb_min_gap = absorb_min_gap
        self.absorb_threshold_relaxed = absorb_threshold_relaxed
        self.absorb_min_gap_relaxed = absorb_min_gap_relaxed
        self.min_cluster_coherence = min_cluster_coherence
        self.max_cluster_size = max_cluster_size
        self.source_overlap_merge_threshold = source_overlap_merge_threshold

    def cluster(
        self,
        snippets: list[EmbeddedSnippet],
    ) -> list[EventCluster]:
        """
        Cluster snippets into events.

        Args:
            snippets: Embedded snippets to cluster

        Returns:
            List of EventClusters (including singleton clusters)
        """
        if len(snippets) < 2:
            if snippets:
                return [self._make_cluster(snippets, cluster_id=0)]
            return []

        # Stack embeddings
        embeddings = np.vstack([s.embedding for s in snippets])

        # Phase 1: HDBSCAN for core clusters
        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=self.min_cluster_size,
            min_samples=self.min_samples,
            cluster_selection_epsilon=self.cluster_selection_epsilon,
            metric="euclidean",
        )

        labels = clusterer.fit_predict(embeddings)

        clusters = {}
        noise_snippets = []

        for snippet, label in zip(snippets, labels):
            if label == -1:
                noise_snippets.append(snippet)
            else:
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(snippet)

        # Build core EventClusters
        result = []
        for label, cluster_snippets in clusters.items():
            result.append(self._make_cluster(cluster_snippets, cluster_id=label))

        # Phase 2: absorb singletons into nearby clusters
        remaining_singletons = self._absorb_singletons(result, noise_snippets)

        # Remaining singletons become their own clusters
        for i, snippet in enumerate(remaining_singletons):
            result.append(self._make_cluster([snippet], cluster_id=f"noise_{i}"))

        absorbed = len(noise_snippets) - len(remaining_singletons)

        # Phase 3: coherence validation — dissolve incoherent clusters
        result, dissolved = self._validate_coherence(result)

        # Phase 4: split megaclusters via tighter re-clustering
        result, splits = self._split_megaclusters(result)

        logger.info(
            f"Clustered {len(snippets)} snippets into {len(result)} events "
            f"({len(clusters)} core clusters, {absorbed} absorbed, "
            f"{len(remaining_singletons)} singletons, "
            f"{dissolved} dissolved for low coherence, "
            f"{splits} megaclusters split)"
        )

        return result

    def _absorb_singletons(
        self,
        clusters: list[EventCluster],
        singletons: list[EmbeddedSnippet],
    ) -> list[EmbeddedSnippet]:
        """
        Absorb singletons into nearest cluster when similarity is high
        and the match is clearly better than alternatives.

        Returns remaining unabsorbed singletons.
        """
        if not clusters or not singletons:
            return singletons

        centroids = np.vstack([c.centroid for c in clusters])
        remaining = []

        for snippet in singletons:
            sims = snippet.embedding @ centroids.T
            ranked = np.argsort(sims)[::-1]
            best_sim = sims[ranked[0]]
            second_sim = sims[ranked[1]] if len(ranked) > 1 else 0
            gap = best_sim - second_sim

            # Standard absorption: high similarity + small gap
            standard_absorb = (
                best_sim >= self.absorb_threshold and
                gap >= self.absorb_min_gap
            )
            # Relaxed absorption: moderate similarity + large gap (clear winner)
            relaxed_absorb = (
                best_sim >= self.absorb_threshold_relaxed and
                gap >= self.absorb_min_gap_relaxed
            )

            if standard_absorb or relaxed_absorb:
                # Absorb into best cluster
                target = clusters[ranked[0]]
                target.snippets.append(snippet)
                absorb_type = "standard" if standard_absorb else "relaxed"
                logger.debug(
                    f"Absorbed ({absorb_type}) '{snippet.title[:50]}' into "
                    f"'{target.representative_title[:50]}' "
                    f"(sim={best_sim:.3f}, gap={gap:.3f})"
                )
            else:
                remaining.append(snippet)

        # Recompute centroids and metadata for modified clusters
        for c in clusters:
            embeddings = np.vstack([s.embedding for s in c.snippets])
            c.centroid = embeddings.mean(axis=0)
            c.centroid = c.centroid / np.linalg.norm(c.centroid)
            c.sources = {s.source_name for s in c.snippets}
            c.source_types = {s.source_type for s in c.snippets}

        return remaining

    def _split_megaclusters(
        self,
        clusters: list[EventCluster],
    ) -> tuple[list[EventCluster], int]:
        """
        Re-cluster any cluster exceeding max_cluster_size with tighter
        HDBSCAN parameters. Produces sub-clusters + singletons.

        Uses 'leaf' cluster selection to find atomic events at the bottom
        of the hierarchy, then validates with source overlap to prevent
        over-fragmentation.

        Returns (new_clusters, split_count).
        """
        result = []
        split_count = 0

        for cluster in clusters:
            if len(cluster.snippets) <= self.max_cluster_size:
                result.append(cluster)
                continue

            logger.info(
                f"Splitting megacluster '{cluster.representative_title[:60]}' "
                f"(size={len(cluster.snippets)})"
            )

            embeddings = np.vstack([s.embedding for s in cluster.snippets])

            # Re-cluster with tighter params:
            # - 'leaf' selection finds smallest homogeneous groups
            # - lower epsilon prevents aggressive merging
            # - higher min_samples forces denser neighborhoods
            sub_clusterer = hdbscan.HDBSCAN(
                min_cluster_size=2,
                min_samples=2,
                cluster_selection_epsilon=0.1,
                cluster_selection_method='leaf',  # Find atomic events
                metric="euclidean",
            )
            sub_labels = sub_clusterer.fit_predict(embeddings)

            sub_groups: dict[int, list[EmbeddedSnippet]] = {}
            for snippet, label in zip(cluster.snippets, sub_labels):
                sub_groups.setdefault(label, []).append(snippet)

            # Build initial sub-clusters (noise=-1 become singletons)
            sub_clusters = []
            sub_id = 0
            for label, members in sub_groups.items():
                if label == -1:
                    for member in members:
                        sub_clusters.append(self._make_cluster(
                            [member], cluster_id=f"{cluster.id}_split_{sub_id}"
                        ))
                        sub_id += 1
                else:
                    sub_clusters.append(self._make_cluster(
                        members, cluster_id=f"{cluster.id}_split_{sub_id}"
                    ))
                    sub_id += 1

            # Validate: re-merge sub-clusters that share too many sources
            # (prevents over-fragmentation from vocabulary differences)
            sub_clusters = self._merge_by_source_overlap(sub_clusters)

            result.extend(sub_clusters)
            split_count += 1
            logger.info(
                f"  -> {len(sub_clusters)} sub-clusters from {len(cluster.snippets)} snippets"
            )

        return result, split_count

    def _merge_by_source_overlap(
        self,
        clusters: list[EventCluster],
    ) -> list[EventCluster]:
        """
        Re-merge clusters that share too many sources.

        If two clusters share N+ sources (default 3), they're almost certainly
        the same event despite embedding distance. This prevents over-fragmentation
        when sources use very different vocabulary.
        """
        if len(clusters) < 2:
            return clusters

        # Build merge groups using union-find
        n = len(clusters)
        parent = list(range(n))

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py

        # Find pairs to merge
        for i in range(n):
            for j in range(i + 1, n):
                shared = clusters[i].sources & clusters[j].sources
                if len(shared) >= self.source_overlap_merge_threshold:
                    union(i, j)
                    logger.debug(
                        f"Merging sub-clusters by source overlap: "
                        f"'{clusters[i].representative_title[:40]}' + "
                        f"'{clusters[j].representative_title[:40]}' "
                        f"(shared: {shared})"
                    )

        # Group by root
        groups: dict[int, list[int]] = {}
        for i in range(n):
            root = find(i)
            groups.setdefault(root, []).append(i)

        # Build merged clusters
        result = []
        for indices in groups.values():
            if len(indices) == 1:
                result.append(clusters[indices[0]])
            else:
                # Merge multiple clusters
                all_snippets = []
                for idx in indices:
                    all_snippets.extend(clusters[idx].snippets)
                merged = self._make_cluster(
                    all_snippets,
                    cluster_id=f"merged_{clusters[indices[0]].id}"
                )
                result.append(merged)

        return result

    def _validate_coherence(
        self,
        clusters: list[EventCluster],
    ) -> tuple[list[EventCluster], int]:
        """
        Dissolve clusters whose avg pairwise cosine similarity is below
        min_cluster_coherence. Members become singleton clusters.

        Returns (validated_clusters, dissolved_count).
        """
        validated = []
        dissolved = 0
        next_singleton_id = 0

        for cluster in clusters:
            if len(cluster.snippets) < 2:
                validated.append(cluster)
                continue

            embeddings = np.vstack([s.embedding for s in cluster.snippets])
            sim_matrix = embeddings @ embeddings.T
            triu = np.triu_indices(len(cluster.snippets), k=1)
            avg_sim = float(np.mean(sim_matrix[triu]))

            if avg_sim >= self.min_cluster_coherence:
                validated.append(cluster)
            else:
                logger.info(
                    f"Dissolving cluster '{cluster.representative_title[:60]}' "
                    f"(size={len(cluster.snippets)}, avg_sim={avg_sim:.3f} "
                    f"< {self.min_cluster_coherence})"
                )
                for snippet in cluster.snippets:
                    validated.append(self._make_cluster(
                        [snippet], cluster_id=f"dissolved_{next_singleton_id}"
                    ))
                    next_singleton_id += 1
                dissolved += 1

        return validated, dissolved

    def _make_cluster(
        self,
        snippets: list[EmbeddedSnippet],
        cluster_id: int | str,
    ) -> EventCluster:
        """Create an EventCluster from snippets."""
        embeddings = np.vstack([s.embedding for s in snippets])
        centroid = embeddings.mean(axis=0)
        centroid = centroid / np.linalg.norm(centroid)  # normalize

        return EventCluster(
            id=str(cluster_id),
            snippets=snippets,
            centroid=centroid,
        )
