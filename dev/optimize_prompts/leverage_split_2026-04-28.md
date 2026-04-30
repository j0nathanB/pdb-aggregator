# Three-Way Token Split — 2026-04-28

Source: 2 weekly Sunday runs (`briefs/20260419` + `briefs/20260426`).
Token estimate: chars/4 (English-text heuristic; ranking-grade, not billing-grade).

## How to read this

Per agent, calls are clustered by their system_prompt template (first 200
chars). Within each cluster:
- `system LCP` = longest common prefix across all system prompts (tokens)
- `user LCP` = longest common prefix across all user messages (tokens)
- `stable prefix` = system LCP + user LCP — the cacheable ceiling per call
- `system var` / `user var` = mean variable tail per call

Leverage (savings/run) = `stable prefix × (n_calls - 1)`, since the first
call writes the cache and the next (n-1) hit it.

## Leverage ranking (savings per pipeline run, both weeks combined)

| rank | agent | stable prefix tokens (max cluster) | calls (max cluster) | savings/run estimate |
|---:|---|---:|---:|---:|
| 1 | copyeditor | 10,622 | 38 | 393,014 |
| 2 | style_editor | 10,325 | 37 | 371,700 |
| 3 | editor | 12,699 | 30 | 368,271 |
| 4 | regional_writer | 10,125 | 6 | 50,625 |
| 5 | country | 62,137 | 1 | 0 |
| 6 | devils_advocate | 10,802 | 1 | 0 |
| 7 | executive | 46,854 | 1 | 0 |
| 8 | global_writer | 18,545 | 1 | 0 |
| 9 | government | 8,265 | 1 | 0 |
| 10 | regional | 12,410 | 1 | 0 |
| 11 | story_map | 85,565 | 1 | 0 |

## Per-cluster split — week 20260419

### copyeditor

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `<role> You are a copyeditor for a weekly geopolitical intell…` | 38 | 10,621 | 311 | 1 | 1,776 | **10,622** | 12,710 |
| #1 `<role> You are a headline copyeditor for a geopolitical inte…` | 1 | 13,705 | 0 | 1,359 | 0 | **15,064** | 15,064 |

### country

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,902 | 0 | 58,235 | 0 | **62,137** | 62,137 |
| #1 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,891 | 0 | 67,879 | 0 | **71,770** | 71,770 |
| #2 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,889 | 0 | 55,759 | 0 | **59,648** | 59,648 |
| #3 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 53,671 | 0 | **57,559** | 57,559 |
| #4 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,887 | 0 | 72,851 | 0 | **76,738** | 76,738 |
| #5 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,895 | 0 | 48,531 | 0 | **52,426** | 52,427 |
| #6 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,889 | 0 | 42,653 | 0 | **46,542** | 46,542 |
| #7 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,889 | 0 | 55,518 | 0 | **59,407** | 59,407 |
| #8 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,887 | 0 | 72,387 | 0 | **76,274** | 76,274 |
| #9 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,889 | 0 | 55,876 | 0 | **59,765** | 59,765 |
| #10 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 60,190 | 0 | **64,078** | 64,078 |
| #11 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,896 | 0 | 56,046 | 0 | **59,942** | 59,943 |
| #12 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 70,490 | 0 | **74,378** | 74,378 |
| #13 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,892 | 0 | 54,290 | 0 | **58,182** | 58,182 |
| #14 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,886 | 0 | 54,423 | 0 | **58,309** | 58,309 |
| #15 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,887 | 0 | 70,177 | 0 | **74,064** | 74,065 |
| #16 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,887 | 0 | 53,295 | 0 | **57,182** | 57,182 |
| #17 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,893 | 0 | 61,049 | 0 | **64,942** | 64,942 |
| #18 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,892 | 0 | 61,765 | 0 | **65,657** | 65,657 |
| #19 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 75,414 | 0 | **79,302** | 79,303 |
| #20 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 63,120 | 0 | **67,008** | 67,008 |
| #21 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 51,436 | 0 | **55,324** | 55,325 |
| #22 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,889 | 0 | 54,987 | 0 | **58,876** | 58,876 |
| #23 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 66,903 | 0 | **70,791** | 70,791 |
| #24 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,889 | 0 | 51,219 | 0 | **55,108** | 55,108 |
| #25 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,894 | 0 | 55,560 | 0 | **59,454** | 59,454 |
| #26 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 57,587 | 0 | **61,475** | 61,475 |
| #27 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 63,424 | 0 | **67,312** | 67,313 |
| #28 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 72,573 | 0 | **76,461** | 76,461 |
| #29 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,889 | 0 | 67,481 | 0 | **71,370** | 71,371 |

### devils_advocate

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `## Role  You are an adversarial reviewer for the Australia c…` | 1 | 2,160 | 0 | 8,642 | 0 | **10,802** | 10,802 |
| #1 `## Role  You are an adversarial reviewer for the Brazil coun…` | 1 | 2,160 | 0 | 6,510 | 0 | **8,670** | 8,670 |
| #2 `## Role  You are an adversarial reviewer for the Canada coun…` | 1 | 2,160 | 0 | 6,768 | 0 | **8,928** | 8,928 |
| #3 `## Role  You are an adversarial reviewer for the Chile count…` | 1 | 2,159 | 0 | 7,150 | 0 | **9,309** | 9,309 |
| #4 `## Role  You are an adversarial reviewer for the Czech Repub…` | 1 | 2,162 | 0 | 7,504 | 0 | **9,666** | 9,666 |
| #5 `## Role  You are an adversarial reviewer for the Estonia cou…` | 1 | 2,160 | 0 | 7,846 | 0 | **10,006** | 10,006 |
| #6 `## Role  You are an adversarial reviewer for the Finland cou…` | 1 | 2,160 | 0 | 7,741 | 0 | **9,901** | 9,901 |
| #7 `## Role  You are an adversarial reviewer for the France coun…` | 1 | 2,160 | 0 | 6,757 | 0 | **8,917** | 8,917 |
| #8 `## Role  You are an adversarial reviewer for the Germany cou…` | 1 | 2,160 | 0 | 5,028 | 0 | **7,188** | 7,188 |
| #9 `## Role  You are an adversarial reviewer for the Hungary cou…` | 1 | 2,160 | 0 | 8,704 | 0 | **10,864** | 10,864 |
| #10 `## Role  You are an adversarial reviewer for the India count…` | 1 | 2,159 | 0 | 6,597 | 0 | **8,756** | 8,756 |
| #11 `## Role  You are an adversarial reviewer for the Indonesia c…` | 1 | 2,160 | 0 | 5,329 | 0 | **7,489** | 7,489 |
| #12 `## Role  You are an adversarial reviewer for the Italy count…` | 1 | 2,159 | 0 | 6,981 | 0 | **9,140** | 9,141 |
| #13 `## Role  You are an adversarial reviewer for the Japan count…` | 1 | 2,159 | 0 | 5,314 | 0 | **7,473** | 7,474 |
| #14 `## Role  You are an adversarial reviewer for the Latvia coun…` | 1 | 2,160 | 0 | 7,539 | 0 | **9,699** | 9,699 |
| #15 `## Role  You are an adversarial reviewer for the Lithuania c…` | 1 | 2,160 | 0 | 7,846 | 0 | **10,006** | 10,006 |
| #16 `## Role  You are an adversarial reviewer for the Mexico coun…` | 1 | 2,160 | 0 | 8,416 | 0 | **10,576** | 10,576 |
| #17 `## Role  You are an adversarial reviewer for the Norway coun…` | 1 | 2,160 | 0 | 6,041 | 0 | **8,201** | 8,201 |
| #18 `## Role  You are an adversarial reviewer for the Pakistan co…` | 1 | 2,160 | 0 | 9,239 | 0 | **11,399** | 11,399 |
| #19 `## Role  You are an adversarial reviewer for the Poland coun…` | 1 | 2,160 | 0 | 5,798 | 0 | **7,958** | 7,958 |
| #20 `## Role  You are an adversarial reviewer for the Romania cou…` | 1 | 2,160 | 0 | 6,220 | 0 | **8,380** | 8,381 |
| #21 `## Role  You are an adversarial reviewer for the Saudi Arabi…` | 1 | 2,161 | 0 | 6,915 | 0 | **9,076** | 9,076 |
| #22 `## Role  You are an adversarial reviewer for the South Korea…` | 1 | 2,161 | 0 | 6,999 | 0 | **9,160** | 9,160 |
| #23 `## Role  You are an adversarial reviewer for the Spain count…` | 1 | 2,159 | 0 | 9,135 | 0 | **11,294** | 11,294 |
| #24 `## Role  You are an adversarial reviewer for the Sweden coun…` | 1 | 2,160 | 0 | 5,003 | 0 | **7,163** | 7,163 |
| #25 `## Role  You are an adversarial reviewer for the Taiwan coun…` | 1 | 2,160 | 0 | 7,241 | 0 | **9,401** | 9,401 |
| #26 `## Role  You are an adversarial reviewer for the Turkey coun…` | 1 | 2,160 | 0 | 7,430 | 0 | **9,590** | 9,590 |
| #27 `## Role  You are an adversarial reviewer for the Ukraine cou…` | 1 | 2,160 | 0 | 8,481 | 0 | **10,641** | 10,641 |
| #28 `## Role  You are an adversarial reviewer for the United Arab…` | 1 | 2,163 | 0 | 7,612 | 0 | **9,775** | 9,775 |
| #29 `## Role  You are an adversarial reviewer for the United King…` | 1 | 2,162 | 0 | 5,137 | 0 | **7,299** | 7,299 |

### editor

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `<role> You are an editor for a weekly geopolitical intellige…` | 30 | 12,695 | 0 | 4 | 10,148 | **12,699** | 22,847 |
| #1 `<role> You are an editor for a weekly geopolitical intellige…` | 6 | 10,814 | 0 | 3 | 12,085 | **10,817** | 22,904 |
| #2 `<role> You are an editor for a weekly geopolitical intellige…` | 1 | 10,716 | 0 | 4,587 | 0 | **15,303** | 15,304 |
| #3 `<role> You are an editor for a weekly geopolitical intellige…` | 1 | 10,443 | 0 | 905 | 0 | **11,348** | 11,348 |

### executive

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `## Role  You are the executive analyst for the Middle Powers…` | 1 | 3,628 | 0 | 43,226 | 0 | **46,854** | 46,854 |

### global_writer

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `<role> You are a writer for a weekly geopolitical intelligen…` | 1 | 10,098 | 0 | 8,447 | 0 | **18,545** | 18,545 |

### government

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `You are a government communications analyst processing offic…` | 1 | 2,454 | 0 | 5,811 | 0 | **8,265** | 8,266 |
| #1 `You are a government communications analyst processing offic…` | 1 | 2,452 | 0 | 9,976 | 0 | **12,428** | 12,428 |
| #2 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 7,650 | 0 | **10,101** | 10,101 |
| #3 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 6,507 | 0 | **8,958** | 8,958 |
| #4 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 5,984 | 0 | **8,435** | 8,435 |
| #5 `You are a government communications analyst processing offic…` | 1 | 2,453 | 0 | 3,226 | 0 | **5,679** | 5,680 |
| #6 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 3,269 | 0 | **5,720** | 5,721 |
| #7 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 3,418 | 0 | **5,869** | 5,869 |
| #8 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 7,600 | 0 | **10,051** | 10,051 |
| #9 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 5,451 | 0 | **7,902** | 7,902 |
| #10 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 2,361 | 0 | **4,812** | 4,812 |
| #11 `You are a government communications analyst processing offic…` | 1 | 2,453 | 0 | 3,456 | 0 | **5,909** | 5,909 |
| #12 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 14,657 | 0 | **17,108** | 17,109 |
| #13 `You are a government communications analyst processing offic…` | 1 | 2,452 | 0 | 3,290 | 0 | **5,742** | 5,742 |
| #14 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 5,670 | 0 | **8,121** | 8,121 |
| #15 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 4,642 | 0 | **7,093** | 7,093 |
| #16 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 3,706 | 0 | **6,157** | 6,157 |
| #17 `You are a government communications analyst processing offic…` | 1 | 2,452 | 0 | 5,237 | 0 | **7,689** | 7,690 |
| #18 `You are a government communications analyst processing offic…` | 1 | 2,452 | 0 | 1,720 | 0 | **4,172** | 4,172 |
| #19 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 7,592 | 0 | **10,043** | 10,043 |
| #20 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 37,483 | 0 | **39,934** | 39,934 |
| #21 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 2,642 | 0 | **5,093** | 5,093 |
| #22 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 9,307 | 0 | **11,758** | 11,759 |
| #23 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 6,545 | 0 | **8,996** | 8,996 |
| #24 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 2,772 | 0 | **5,223** | 5,224 |
| #25 `You are a government communications analyst processing offic…` | 1 | 2,452 | 0 | 4,286 | 0 | **6,738** | 6,738 |
| #26 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 5,447 | 0 | **7,898** | 7,898 |
| #27 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 2,054 | 0 | **4,505** | 4,505 |
| #28 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 6,572 | 0 | **9,023** | 9,023 |
| #29 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 5,937 | 0 | **8,388** | 8,388 |

### regional

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `## Role  You are a regional intelligence analyst producing a…` | 1 | 3,010 | 0 | 9,400 | 0 | **12,410** | 12,410 |
| #1 `## Role  You are a regional intelligence analyst producing a…` | 1 | 3,014 | 0 | 11,598 | 0 | **14,612** | 14,612 |
| #2 `## Role  You are a regional intelligence analyst producing a…` | 1 | 3,022 | 0 | 12,112 | 0 | **15,134** | 15,134 |
| #3 `## Role  You are a regional intelligence analyst producing a…` | 1 | 3,023 | 0 | 13,327 | 0 | **16,350** | 16,351 |
| #4 `## Role  You are a regional intelligence analyst producing a…` | 1 | 3,016 | 0 | 14,275 | 0 | **17,291** | 17,292 |
| #5 `## Role  You are a regional intelligence analyst producing a…` | 1 | 3,016 | 0 | 11,393 | 0 | **14,409** | 14,410 |

### regional_writer

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `<role> You are a writer for a weekly geopolitical intelligen…` | 6 | 10,122 | 0 | 3 | 5,295 | **10,125** | 15,421 |

### story_map

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,982 | 0 | 82,583 | 0 | **85,565** | 85,565 |
| #1 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,979 | 0 | 71,857 | 0 | **74,836** | 74,836 |
| #2 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,978 | 0 | 87,596 | 0 | **90,574** | 90,574 |
| #3 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,978 | 0 | 87,626 | 0 | **90,604** | 90,605 |
| #4 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,978 | 0 | 87,587 | 0 | **90,565** | 90,565 |
| #5 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,980 | 0 | 75,448 | 0 | **78,428** | 78,428 |
| #6 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 87,656 | 0 | **90,738** | 90,738 |
| #7 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,979 | 0 | 62,604 | 0 | **65,583** | 65,583 |
| #8 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,978 | 0 | 87,496 | 0 | **90,474** | 90,475 |
| #9 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,979 | 0 | 56,901 | 0 | **59,880** | 59,880 |
| #10 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,978 | 0 | 87,543 | 0 | **90,521** | 90,521 |
| #11 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,980 | 0 | 85,531 | 0 | **88,511** | 88,512 |
| #12 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,979 | 0 | 87,662 | 0 | **90,641** | 90,641 |
| #13 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,979 | 0 | 87,536 | 0 | **90,515** | 90,515 |
| #14 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,978 | 0 | 87,562 | 0 | **90,540** | 90,541 |
| #15 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,978 | 0 | 87,687 | 0 | **90,665** | 90,665 |
| #16 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,980 | 0 | 78,718 | 0 | **81,698** | 81,698 |
| #17 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,979 | 0 | 35,291 | 0 | **38,270** | 38,271 |
| #18 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,978 | 0 | 51,791 | 0 | **54,769** | 54,769 |
| #19 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,978 | 0 | 87,610 | 0 | **90,588** | 90,588 |
| #20 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 66,981 | 0 | **70,063** | 70,064 |
| #21 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,979 | 0 | 87,814 | 0 | **90,793** | 90,794 |
| #22 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 87,529 | 0 | **90,611** | 90,612 |
| #23 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 87,575 | 0 | **90,657** | 90,658 |
| #24 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,980 | 0 | 87,607 | 0 | **90,587** | 90,587 |
| #25 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,978 | 0 | 61,469 | 0 | **64,447** | 64,448 |
| #26 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,978 | 0 | 87,692 | 0 | **90,670** | 90,670 |
| #27 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,978 | 0 | 81,760 | 0 | **84,738** | 84,739 |
| #28 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 2,979 | 0 | 86,679 | 0 | **89,658** | 89,658 |

### style_editor

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `<role> You are a style editor for a weekly geopolitical inte…` | 37 | 10,324 | 0 | 1 | 1,210 | **10,325** | 11,536 |

## Per-cluster split — week 20260426

### copyeditor

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `<role> You are a copyeditor for a weekly geopolitical intell…` | 37 | 10,660 | 281 | 1 | 2,070 | **10,661** | 13,013 |
| #1 `<role> You are a headline copyeditor for a geopolitical inte…` | 1 | 13,821 | 0 | 1,411 | 0 | **15,232** | 15,233 |

### country

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,902 | 0 | 62,865 | 0 | **66,767** | 66,767 |
| #1 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,891 | 0 | 70,600 | 0 | **74,491** | 74,491 |
| #2 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,889 | 0 | 66,918 | 0 | **70,807** | 70,807 |
| #3 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 77,825 | 0 | **81,713** | 81,714 |
| #4 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,887 | 0 | 83,219 | 0 | **87,106** | 87,106 |
| #5 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,895 | 0 | 66,648 | 0 | **70,543** | 70,544 |
| #6 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,889 | 0 | 65,317 | 0 | **69,206** | 69,206 |
| #7 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,889 | 0 | 55,816 | 0 | **59,705** | 59,705 |
| #8 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,887 | 0 | 80,379 | 0 | **84,266** | 84,266 |
| #9 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,889 | 0 | 74,499 | 0 | **78,388** | 78,388 |
| #10 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 64,154 | 0 | **68,042** | 68,042 |
| #11 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,896 | 0 | 64,670 | 0 | **68,566** | 68,567 |
| #12 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 70,463 | 0 | **74,351** | 74,351 |
| #13 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,892 | 0 | 69,117 | 0 | **73,009** | 73,009 |
| #14 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,886 | 0 | 70,589 | 0 | **74,475** | 74,475 |
| #15 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,887 | 0 | 73,954 | 0 | **77,841** | 77,841 |
| #16 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,887 | 0 | 98,198 | 0 | **102,085** | 102,085 |
| #17 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,893 | 0 | 82,218 | 0 | **86,111** | 86,111 |
| #18 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,892 | 0 | 96,390 | 0 | **100,282** | 100,282 |
| #19 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 88,647 | 0 | **92,535** | 92,535 |
| #20 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 72,118 | 0 | **76,006** | 76,006 |
| #21 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 65,282 | 0 | **69,170** | 69,171 |
| #22 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,889 | 0 | 57,810 | 0 | **61,699** | 61,699 |
| #23 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 82,585 | 0 | **86,473** | 86,473 |
| #24 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,889 | 0 | 65,983 | 0 | **69,872** | 69,873 |
| #25 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,894 | 0 | 95,752 | 0 | **99,646** | 99,646 |
| #26 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 88,102 | 0 | **91,990** | 91,990 |
| #27 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 62,490 | 0 | **66,378** | 66,378 |
| #28 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,888 | 0 | 69,252 | 0 | **73,140** | 73,140 |
| #29 `## Role  You are a country desk analyst producing a weekly i…` | 1 | 3,889 | 0 | 70,581 | 0 | **74,470** | 74,471 |

### devils_advocate

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `## Role  You are an adversarial reviewer for the Australia c…` | 1 | 2,160 | 0 | 6,298 | 0 | **8,458** | 8,459 |
| #1 `## Role  You are an adversarial reviewer for the Brazil coun…` | 1 | 2,160 | 0 | 7,484 | 0 | **9,644** | 9,644 |
| #2 `## Role  You are an adversarial reviewer for the Canada coun…` | 1 | 2,160 | 0 | 9,859 | 0 | **12,019** | 12,019 |
| #3 `## Role  You are an adversarial reviewer for the Chile count…` | 1 | 2,159 | 0 | 3,157 | 0 | **5,316** | 5,317 |
| #4 `## Role  You are an adversarial reviewer for the Czech Repub…` | 1 | 2,162 | 0 | 7,323 | 0 | **9,485** | 9,485 |
| #5 `## Role  You are an adversarial reviewer for the Estonia cou…` | 1 | 2,160 | 0 | 6,463 | 0 | **8,623** | 8,623 |
| #6 `## Role  You are an adversarial reviewer for the Finland cou…` | 1 | 2,160 | 0 | 8,368 | 0 | **10,528** | 10,528 |
| #7 `## Role  You are an adversarial reviewer for the France coun…` | 1 | 2,160 | 0 | 8,343 | 0 | **10,503** | 10,503 |
| #8 `## Role  You are an adversarial reviewer for the Germany cou…` | 1 | 2,160 | 0 | 7,715 | 0 | **9,875** | 9,875 |
| #9 `## Role  You are an adversarial reviewer for the Hungary cou…` | 1 | 2,160 | 0 | 8,900 | 0 | **11,060** | 11,060 |
| #10 `## Role  You are an adversarial reviewer for the India count…` | 1 | 2,159 | 0 | 7,898 | 0 | **10,057** | 10,058 |
| #11 `## Role  You are an adversarial reviewer for the Indonesia c…` | 1 | 2,160 | 0 | 6,151 | 0 | **8,311** | 8,312 |
| #12 `## Role  You are an adversarial reviewer for the Italy count…` | 1 | 2,159 | 0 | 6,034 | 0 | **8,193** | 8,194 |
| #13 `## Role  You are an adversarial reviewer for the Japan count…` | 1 | 2,159 | 0 | 7,109 | 0 | **9,268** | 9,269 |
| #14 `## Role  You are an adversarial reviewer for the Latvia coun…` | 1 | 2,160 | 0 | 7,118 | 0 | **9,278** | 9,278 |
| #15 `## Role  You are an adversarial reviewer for the Lithuania c…` | 1 | 2,160 | 0 | 8,171 | 0 | **10,331** | 10,332 |
| #16 `## Role  You are an adversarial reviewer for the Mexico coun…` | 1 | 2,160 | 0 | 7,615 | 0 | **9,775** | 9,775 |
| #17 `## Role  You are an adversarial reviewer for the Norway coun…` | 1 | 2,160 | 0 | 7,336 | 0 | **9,496** | 9,496 |
| #18 `## Role  You are an adversarial reviewer for the Pakistan co…` | 1 | 2,160 | 0 | 7,954 | 0 | **10,114** | 10,115 |
| #19 `## Role  You are an adversarial reviewer for the Poland coun…` | 1 | 2,160 | 0 | 7,342 | 0 | **9,502** | 9,502 |
| #20 `## Role  You are an adversarial reviewer for the Romania cou…` | 1 | 2,160 | 0 | 6,280 | 0 | **8,440** | 8,440 |
| #21 `## Role  You are an adversarial reviewer for the Saudi Arabi…` | 1 | 2,161 | 0 | 8,603 | 0 | **10,764** | 10,764 |
| #22 `## Role  You are an adversarial reviewer for the South Korea…` | 1 | 2,161 | 0 | 7,382 | 0 | **9,543** | 9,543 |
| #23 `## Role  You are an adversarial reviewer for the Spain count…` | 1 | 2,159 | 0 | 7,790 | 0 | **9,949** | 9,950 |
| #24 `## Role  You are an adversarial reviewer for the Sweden coun…` | 1 | 2,160 | 0 | 6,609 | 0 | **8,769** | 8,769 |
| #25 `## Role  You are an adversarial reviewer for the Taiwan coun…` | 1 | 2,160 | 0 | 8,009 | 0 | **10,169** | 10,169 |
| #26 `## Role  You are an adversarial reviewer for the Turkey coun…` | 1 | 2,160 | 0 | 6,722 | 0 | **8,882** | 8,882 |
| #27 `## Role  You are an adversarial reviewer for the Ukraine cou…` | 1 | 2,160 | 0 | 7,648 | 0 | **9,808** | 9,808 |
| #28 `## Role  You are an adversarial reviewer for the United Arab…` | 1 | 2,163 | 0 | 7,110 | 0 | **9,273** | 9,274 |
| #29 `## Role  You are an adversarial reviewer for the United King…` | 1 | 2,162 | 0 | 5,850 | 0 | **8,012** | 8,012 |

### editor

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `<role> You are an editor for a weekly geopolitical intellige…` | 30 | 12,695 | 0 | 4 | 12,674 | **12,699** | 25,373 |
| #1 `<role> You are an editor for a weekly geopolitical intellige…` | 6 | 10,814 | 0 | 3 | 12,076 | **10,817** | 22,895 |
| #2 `<role> You are an editor for a weekly geopolitical intellige…` | 1 | 10,716 | 0 | 4,504 | 0 | **15,220** | 15,220 |

### executive

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `## Role  You are the executive analyst for the Middle Powers…` | 1 | 3,628 | 0 | 44,418 | 0 | **48,046** | 48,046 |

### global_writer

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `<role> You are a writer for a weekly geopolitical intelligen…` | 1 | 10,098 | 0 | 7,901 | 0 | **17,999** | 18,000 |

### government

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `You are a government communications analyst processing offic…` | 1 | 2,454 | 0 | 4,186 | 0 | **6,640** | 6,641 |
| #1 `You are a government communications analyst processing offic…` | 1 | 2,452 | 0 | 9,102 | 0 | **11,554** | 11,554 |
| #2 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 4,466 | 0 | **6,917** | 6,917 |
| #3 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 4,523 | 0 | **6,974** | 6,974 |
| #4 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 6,104 | 0 | **8,555** | 8,555 |
| #5 `You are a government communications analyst processing offic…` | 1 | 2,453 | 0 | 2,213 | 0 | **4,666** | 4,666 |
| #6 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 6,279 | 0 | **8,730** | 8,730 |
| #7 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 3,742 | 0 | **6,193** | 6,194 |
| #8 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 7,703 | 0 | **10,154** | 10,154 |
| #9 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 6,182 | 0 | **8,633** | 8,634 |
| #10 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 3,328 | 0 | **5,779** | 5,779 |
| #11 `You are a government communications analyst processing offic…` | 1 | 2,453 | 0 | 5,030 | 0 | **7,483** | 7,483 |
| #12 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 14,601 | 0 | **17,052** | 17,052 |
| #13 `You are a government communications analyst processing offic…` | 1 | 2,452 | 0 | 2,629 | 0 | **5,081** | 5,081 |
| #14 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 3,498 | 0 | **5,949** | 5,949 |
| #15 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 2,503 | 0 | **4,954** | 4,954 |
| #16 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 4,012 | 0 | **6,463** | 6,463 |
| #17 `You are a government communications analyst processing offic…` | 1 | 2,452 | 0 | 5,723 | 0 | **8,175** | 8,176 |
| #18 `You are a government communications analyst processing offic…` | 1 | 2,452 | 0 | 1,674 | 0 | **4,126** | 4,126 |
| #19 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 9,325 | 0 | **11,776** | 11,777 |
| #20 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 33,473 | 0 | **35,924** | 35,925 |
| #21 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 3,719 | 0 | **6,170** | 6,170 |
| #22 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 8,015 | 0 | **10,466** | 10,466 |
| #23 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 4,317 | 0 | **6,768** | 6,769 |
| #24 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 2,305 | 0 | **4,756** | 4,757 |
| #25 `You are a government communications analyst processing offic…` | 1 | 2,452 | 0 | 4,131 | 0 | **6,583** | 6,584 |
| #26 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 4,430 | 0 | **6,881** | 6,881 |
| #27 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 1,663 | 0 | **4,114** | 4,114 |
| #28 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 6,822 | 0 | **9,273** | 9,273 |
| #29 `You are a government communications analyst processing offic…` | 1 | 2,451 | 0 | 5,506 | 0 | **7,957** | 7,958 |

### regional

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `## Role  You are a regional intelligence analyst producing a…` | 1 | 3,010 | 0 | 9,083 | 0 | **12,093** | 12,094 |
| #1 `## Role  You are a regional intelligence analyst producing a…` | 1 | 3,014 | 0 | 13,737 | 0 | **16,751** | 16,752 |
| #2 `## Role  You are a regional intelligence analyst producing a…` | 1 | 3,022 | 0 | 13,759 | 0 | **16,781** | 16,781 |
| #3 `## Role  You are a regional intelligence analyst producing a…` | 1 | 3,023 | 0 | 13,536 | 0 | **16,559** | 16,559 |
| #4 `## Role  You are a regional intelligence analyst producing a…` | 1 | 3,016 | 0 | 16,218 | 0 | **19,234** | 19,234 |
| #5 `## Role  You are a regional intelligence analyst producing a…` | 1 | 3,016 | 0 | 13,153 | 0 | **16,169** | 16,169 |

### regional_writer

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `<role> You are a writer for a weekly geopolitical intelligen…` | 6 | 10,122 | 0 | 3 | 6,121 | **10,125** | 16,247 |

### story_map

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,086 | 0 | 65,694 | 0 | **68,780** | 68,780 |
| #1 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,083 | 0 | 72,832 | 0 | **75,915** | 75,915 |
| #2 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 87,724 | 0 | **90,806** | 90,807 |
| #3 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 87,659 | 0 | **90,741** | 90,742 |
| #4 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 87,562 | 0 | **90,644** | 90,644 |
| #5 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,084 | 0 | 87,617 | 0 | **90,701** | 90,702 |
| #6 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 79,449 | 0 | **82,531** | 82,532 |
| #7 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 73,195 | 0 | **76,277** | 76,277 |
| #8 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 87,692 | 0 | **90,774** | 90,774 |
| #9 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 60,254 | 0 | **63,336** | 63,337 |
| #10 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 87,636 | 0 | **90,718** | 90,719 |
| #11 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,084 | 0 | 87,519 | 0 | **90,603** | 90,603 |
| #12 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 87,765 | 0 | **90,847** | 90,847 |
| #13 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,083 | 0 | 87,675 | 0 | **90,758** | 90,758 |
| #14 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 87,560 | 0 | **90,642** | 90,642 |
| #15 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 87,743 | 0 | **90,825** | 90,825 |
| #16 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 68,779 | 0 | **71,861** | 71,861 |
| #17 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,083 | 0 | 87,706 | 0 | **90,789** | 90,790 |
| #18 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,083 | 0 | 42,289 | 0 | **45,372** | 45,373 |
| #19 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 57,495 | 0 | **60,577** | 60,578 |
| #20 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 87,575 | 0 | **90,657** | 90,658 |
| #21 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 67,461 | 0 | **70,543** | 70,543 |
| #22 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,083 | 0 | 87,840 | 0 | **90,923** | 90,923 |
| #23 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 86,689 | 0 | **89,771** | 89,771 |
| #24 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 87,617 | 0 | **90,699** | 90,700 |
| #25 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,084 | 0 | 87,719 | 0 | **90,803** | 90,803 |
| #26 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 66,243 | 0 | **69,325** | 69,326 |
| #27 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 87,527 | 0 | **90,609** | 90,609 |
| #28 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 87,555 | 0 | **90,637** | 90,637 |
| #29 `# Story Map Agent — System Prompt  ## Role  You are a news d…` | 1 | 3,082 | 0 | 84,973 | 0 | **88,055** | 88,055 |

### style_editor

| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| #0 `<role> You are a style editor for a weekly geopolitical inte…` | 37 | 10,324 | 0 | 1 | 1,277 | **10,325** | 11,602 |
