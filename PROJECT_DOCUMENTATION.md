# Project Documentation

## Detecting Stance in Media on Global Warming for Indic Languages

**Project:** CSET 346 -- Natural Language Processing\
**Institution:** Bennett University\
**Documentation policy:** This is the project's milestone log. Add a new
dated entry only when a major project step is completed. Do not rewrite
the history of earlier entries; append a new entry and update the status
summary.

------------------------------------------------------------------------

## 1. Project objective

Build an NLP system to classify Hindi and Bengali YouTube comments
expressing a stance on the claim:

> "Climate change and global warming is a serious concern."

The target labels are:

-   **Favour** -- supports or agrees with the claim.
-   **Against** -- disagrees with or rejects the claim.
-   **None** -- does not express a clear position.

The primary evaluation metric is **Macro F1-score**. Other reported
metrics include accuracy, precision, recall, and a confusion matrix.

------------------------------------------------------------------------

## 2. Major-step tracker

  ---------------------------------------------------------------------------------
                     \# Major step       Status           Notes
  --------------------- ---------------- ---------------- -------------------------
                      1 Project setup    Completed        Project directory and
                        and environment                   Python environments
                                                          established; dependencies
                                                          and YouTube API
                                                          configuration set up.

                      2 YouTube data     Completed        1,009 comments collected
                        collection                        from 36 videos.

                      3 Dataset          Completed        Script/language
                        exploration and                   exploration and initial
                        language                          language-identification
                        identification                    review completed.

                      4 Cleaning,        Completed        611 comments from 13
                        relevance                         priority videos reviewed
                        filtering and                     and provisionally
                        first annotation                  annotated.
                        pass                              

                      5 Dataset          In progress      104 Latin/mixed-script
                        preparation for                   language candidates
                        ML                                reviewed in conversation;
                                                          decisions still need to
                                                          be saved and audited in
                                                          the project CSV. Final
                                                          dataset and split are not
                                                          yet prepared.

                      6 Model            Not started      Baseline and candidate
                        development                       models to be developed.

                      7 Model evaluation Not started      Evaluate using Macro F1,
                        and improvement                   accuracy, precision,
                                                          recall, and confusion
                                                          matrix.

                      8 Prediction file  Not started      Generate and validate
                        and final                         predictions in the
                        implementation                    required format.

                      9 GitHub           Not started      Organize source code,
                        repository and                    README, and
                        documentation                     reproducibility
                                                          information.

                     10 Final report and Not started      Prepare the report
                        submission                        (maximum 8 pages),
                                                          prediction file, and
                                                          optional slides.
  ---------------------------------------------------------------------------------

------------------------------------------------------------------------

## 3. Completed-step records

### Step 1 -- Project setup and environment

**Status:** Completed

-   Created the project directory: `~/climate-stance-nlp`.
-   Set up Python environments, including a Python 3.12.16 environment
    named `lid-env`.
-   Installed required packages for data handling and language
    identification.
-   Configured the YouTube API key through a `.env` file. The key must
    remain private and must not be committed to GitHub.

### Step 2 -- YouTube data collection

**Status:** Completed

-   Collected **1,009 YouTube comments** from **36 videos**.
-   Preserved comment and video metadata.
-   Saved the raw dataset to `data/raw/youtube_comments.csv`.
-   The raw dataset is the source record and should remain unchanged.
    Cleaning and annotation should happen in separate files.

### Step 3 -- Dataset exploration and language identification

**Status:** Completed

-   Explored the scripts used in the comments and identified
    native-script, Latin-script, mixed-script, and other text.
-   Used MIRA Indic Language Identification as an initial
    language-identification aid.
-   Found that automatic language identification is not reliable enough
    on its own for Romanized Hindi/Bengali and can misclassify English
    text.
-   Created supporting review and analysis files, including:
    -   `data/processed/language_review.csv`
    -   `data/processed/video_quality_report.csv`
    -   `data/processed/language_script_audit.csv`

### Step 4 -- Cleaning, relevance filtering and first annotation pass

**Status:** Completed

-   Selected comments from 13 priority videos for annotation.
-   Created 13 annotation batches covering **611 comments**.
-   Consolidated the annotations into
    `data/processed/annotations_all.csv`.
-   Initial relevance counts:
    -   Relevant: 212
    -   Irrelevant: 349
    -   Uncertain: 50
-   Initial stance counts across all 611 reviewed comments:
    -   Favour: 157
    -   Against: 9
    -   None: 445
-   Annotation records were marked **Provisional**. These are first-pass
    labels and require final validation before model training.
-   The 212 comments marked Relevant had this initial stance
    distribution:
    -   Favour: 157
    -   Against: 9
    -   None: 46
-   Created `data/processed/relevance_review.csv` and the annotation
    audit scripts/reports.
-   Important annotation principle: sentiment is not the same as stance.
    A positive or negative tone must not automatically determine Favour
    or Against.

------------------------------------------------------------------------

## 4. Current in-progress work

### Step 5 -- Dataset preparation for ML

**Status:** In progress

#### 5.1 Language and script audit

Among the 212 comments initially marked Relevant, the writing-script
distribution was:

  Script category        Count
  ------------------ ---------
  Latin script             119
  Devanagari                50
  Mixed scripts             29
  Bengali script            12
  Other or symbols           2
  **Total**            **212**

A review subset of **104 comments** using Latin or mixed scripts was
created in:

`data/processed/romanized_language_review.csv`

The 104 candidates have all been reviewed in the conversation and
proposed language labels have been assigned. However, those proposed
decisions have **not yet been written into the CSV**. Do not treat the
review as persisted until the file has been updated and audited.

Proposed language categories used during review: - `Hindi` -
`Hindi_Romanized` - `Bengali` - `Bengali_Romanized` - `English` -
`Other` - `Uncertain`

The language field should identify the language; the separate script
field should identify how it is written. Mixed-script comments should be
assigned according to their dominant language, with genuinely ambiguous
cases marked Uncertain.

#### 5.2 Supplementary dataset assessed

A separate uploaded file, `combined_hindi_bengali_climate_filtered.csv`,
was inspected. It contains 1,085 records: - 560 Hindi records associated
with a climate-resilience instruction corpus. - 525 Bengali records
associated with a news-headline source.

The file contains 429 duplicate text entries and its labels are pending
or are not equivalent to the project's stance labels. It is a different
text domain from YouTube comments. Decision: keep it separate; do not
merge it directly into the primary YouTube-comment dataset. Any future
use requires source verification, relevance checks, duplicate handling,
and stance re-annotation.

#### 5.3 Remaining work before Step 5 can be marked complete

1.  Write all 104 reviewed language decisions into
    `romanized_language_review.csv`.
2.  Check the saved values and ensure the original stance annotations
    have not changed.
3.  Revisit ambiguous language and stance cases, including short or
    unclear comments.
4.  Reassess relevance and remove Irrelevant/Uncertain records from the
    primary labelled training set according to the final inclusion
    policy.
5.  Check exact and near-duplicate comment text to prevent train/test
    leakage.
6.  Decide and document whether Romanized Hindi/Bengali will be included
    in the primary experiment, a separate experiment, or excluded.
7.  Validate the final Favour/Against/None labels. Do not infer stance
    from sentiment.
8.  Create and audit the final model-ready dataset.
9.  Split the data into training, validation, and test sets in a
    leakage-aware way, preferably grouping duplicates and related source
    material before splitting.

**Step 5 is not complete until these preparation and validation tasks
are finished and the final dataset is saved.**

------------------------------------------------------------------------

## 5. Decisions and safeguards

-   Preserve `data/raw/youtube_comments.csv`; never overwrite the raw
    source dataset.
-   Keep the supplementary headline/instruction dataset separate from
    the YouTube-comment dataset unless a justified, separately evaluated
    experiment is designed.
-   Do not equate sentiment labels with stance labels.
-   `None` means no clear stance in an otherwise relevant comment; it
    does not mean irrelevant or missing.
-   Do not use automatic language identification as the sole authority
    for Romanized comments.
-   Keep annotation status and uncertainty visible. Provisional labels
    must not be presented as fully validated ground truth.
-   Report class imbalance honestly. The initial relevant subset
    contains only 9 Against examples, so per-language and per-class
    evaluation may be limited.
-   Keep API keys, credentials, and other secrets out of source control
    and documentation.

------------------------------------------------------------------------

## 6. Next action

Continue Step 5 by saving and auditing the 104 manually reviewed
language decisions. After the final model-ready dataset has been
validated and saved, append a **Step 5 -- Dataset preparation for ML
completed** entry to this document and update the tracker. Only then
move to Step 6.

------------------------------------------------------------------------

## 7. Future milestone log

Append a new entry below only when a major step is completed. Include
the completion date, work performed, key files/artifacts produced,
validation performed, important decisions, and the next major step.

*(No later milestone entries have been recorded yet.)*
