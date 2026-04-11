Return a JSON object with this structure:
{
  "country": "{{COUNTRY_CODE}}",
  "processing_date": "{{ANALYSIS_DATE}}",
  "information_culture": "transparent | managed | controlled",
  "items_processed": 0,
  "items_with_findings": 0,

  "findings": [
    {
      "source_institution": "Institution name",
      "source_category": "foreign_ministry | defense_ministry | head_of_government | parliament | gazette | finance_ministry | central_bank | trade_ministry | nsc_intelligence | country_specific",
      "source_url": "https://...",
      "publication_date": "YYYY-MM-DD",
      "content_type": "ground_truth | intent_signal | both",
      "signal_categories": ["alignment_diplomatic"],

      "what_happened": "...",
      "structural_significance": "...",
      "framing_note": "...",
      "information_culture_note": "For managed/controlled cultures only. Note how the information culture affects interpretation of this specific item.",
      "cross_reference": "..."
    }
  ],

  "discovery_gaps": [
    {
      "domain": "government domain",
      "institution": "Institution name",
      "priority": "P1 | P2",
      "assessment": "Expected — [reason] | Unexpected — [reason for concern] | Uncertain — Google indexing may lag"
    }
  ],

  "extraction_failures": [
    {
      "source_institution": "Institution name",
      "url": "https://...",
      "error": "Extraction method and failure description",
      "content_available": "headline_only | snippet | partial_text",
      "note": "Whether partial content is sufficient for classification or finding is degraded"
    }
  ]
}