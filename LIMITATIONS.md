# Limitations

**Critical limitations and interpretation constraints for this analysis**

---

## ⚠️ Executive Summary

This study examines **ONLY textual caption metadata** through keyword matching.

**What this analysis DOES:**
- ✅ Documents observable textual patterns in captions
- ✅ Quantifies frequency of specific keywords
- ✅ Provides reproducible empirical measurements

**What this analysis DOES NOT do:**
- ❌ Analyze image content
- ❌ Determine copyright status
- ❌ Establish licensing compliance
- ❌ Identify actual infringement
- ❌ Make legal claims

---

## 1. Methodological Limitations

### 1.1 Textual Scope Only

**What was analyzed:**
- Caption text fields only
- Publicly accessible metadata

**What was NOT analyzed:**
- Visual image content
- Embedded image metadata (EXIF data)
- ALT text or other HTML attributes
- File names or directory structures
- Private/proprietary metadata

**Implication:** Cannot determine what images actually depict

---

### 1.2 Keyword Matching Constraints

#### False Negatives (Missed Content)

The keyword approach **misses:**

- **Synonyms:** "Spider-Man" search misses "Spidey", "web-slinger"
- **Misspellings:** "Batmn", "Pikahu", "Micky Mouse"
- **Non-English:** "Batman" in Japanese: "バットマン"
- **Abbreviations:** "AP" without "Associated Press"
- **Implicit references:** Image of Batman with caption "Dark Knight"
- **Visual-only depictions:** Image clearly shows Batman, caption says "superhero"

**Estimated false negative rate:** >95% for copyrighted visual content

**Why:** Most professional photography, artwork, and character depictions contain **no textual copyright markers** in captions.

---

#### False Positives (Incorrect Matches)

The keyword approach **incorrectly includes:**

**Example 1: Personal names**
```
Caption: "Mario Andretti wins race"
Match: "Mario" (Nintendo character query)
Reality: Not about Nintendo character
```

**Example 2: Common words**
```
Caption: "Link to full article in bio"
Match: "Link" (Zelda character query)
Reality: Not about Nintendo character
```

**Example 3: Generic terms**
```
Caption: "Copyright 2024 John Smith Photography"
Match: "copyright" query
Reality: Proper attribution, not stock agency
```

**Example 4: Unrelated context**
```
Caption: "Thor's Hammer found in Norway"
Match: "Thor" (Marvel character query)
Reality: Norse mythology, not Marvel
```

**Mitigation:** Context filters reduce but don't eliminate false positives

**Estimated false positive rate:** Unknown (no manual validation at scale)

---

#### Context Blindness

**Cannot distinguish:**

- Direct depiction vs. discussion
- Original vs. derivative work
- Licensed vs. unlicensed
- Commercial vs. fair use
- Parody vs. straight depiction
- News coverage vs. promotional material
- Fan art vs. official artwork
- Merchandise photography vs. unauthorized reproduction

**Example:**
```
Caption: "Batman action figure for sale on eBay"
```

Could be:
- ✅ Licensed merchandise (legitimate)
- ✅ Bootleg/counterfeit product (infringement)
- ✅ Collector's item (fair use)
- ❓ Cannot determine from text alone

---

### 1.3 Selection Bias

#### Copyright Indicators

**Measured:**
- 7 major stock photo agencies
- 3 textual copyright markers

**NOT measured:**
- Thousands of smaller stock agencies
- Independent photographers
- Artist watermarks/signatures
- Regional/non-English stock providers
- Museum/archive attributions
- Publisher credits

**Implication:** Likely captures <5% of actual copyrighted content

---

#### Franchise Characters

**Measured:**
- 48 characters from 6 major rights holders
- Primarily English-language franchises
- Commercially successful properties

**NOT measured:**
- Thousands of other franchises
- Independent creators
- Non-English media properties
- Lesser-known characters
- Emerging franchises
- Individual artist IP

**Implication:** Sample represents major commercial IP only, not comprehensive IP landscape

---

### 1.4 Linguistic Limitations

**English-only analysis:**
- Queries conducted in English only
- Misses non-English captions
- Misses transliterated names
- Misses localized character names

**Example:**
- "Pikachu" (English) vs. "ピカチュウ" (Japanese)
- "Mickey Mouse" vs. "米老鼠" (Chinese)

**Datasets contain:** Multilingual captions  
**Analysis captures:** English-language mentions only

---

## 2. Interpretive Limitations

### 2.1 Copyright Indicator Interpretation

#### Presence Does NOT Mean:

❌ Image is unlicensed stock content  
❌ Copyright infringement occurred  
❌ Dataset creators violated terms  
❌ Content is illegitimate  

#### Presence COULD Mean:

✅ Proper attribution to licensed source  
✅ Embedded metadata from legitimate use  
✅ News article crediting photographer  
✅ Discussion about stock photography  
✅ Watermarked preview image (legitimate or not)  
✅ Many other scenarios  

**Example:**
```
Caption: "Photo: Getty Images / John Smith"
```

Could indicate:
1. Properly licensed Getty image with attribution
2. Scraped watermarked preview (unauthorized)
3. News article using Getty image under license
4. Blog post discussing Getty image
5. Embedded EXIF data from photo editing software

**Analysis cannot distinguish these cases.**

---

#### Absence Does NOT Mean:

❌ Content is uncopyrighted  
❌ Content is public domain  
❌ Content may be freely used  
❌ No intellectual property rights apply  
❌ Dataset filtering successfully removed copyrighted content  

**Reality:** Most copyrighted professional content contains **no textual markers** in captions.

---

### 2.2 Character Mention Interpretation

#### Presence Does NOT Mean:

❌ Image shows character depiction  
❌ Unauthorized use of character  
❌ Copyright infringement  
❌ Violates rights holder IP  

#### Presence COULD Mean:

✅ Official merchandise photography (licensed)  
✅ Fan art (potentially transformative/fair use)  
✅ News coverage (fair use)  
✅ Parody or satire (legally protected)  
✅ Educational/commentary use  
✅ Cosplay photography  
✅ Video game screenshots  
✅ Film promotional materials  
✅ Many other contexts  

**Example:**
```
Caption: "Batman cosplay at Comic-Con 2024"
```

This is:
- ✅ Legitimate fan activity
- ✅ Not copyright infringement
- ✅ Protected transformative use

**But analysis counts it as "Batman mention" without distinction.**

---

### 2.3 Statistical Limitations

#### No Confidence Intervals

**Why:** Analysis covers complete corpus, not statistical sample

**Implication:** Percentages are exact for **caption text** but don't generalize to:
- Underlying image content
- Web-scale distributions
- Future datasets
- Other scraping approaches

---

#### Observed vs. Actual Prevalence

**Reported:** Percentages of **textual mentions**  
**Unknown:** Percentage of **visual copyrighted content**  

**Example:**
- 0.0505% of captions mention "Batman"
- Does NOT mean 0.0505% of **images** depict Batman
- Could be higher (images without text) or lower (text without images)

---

#### Non-Representative Sample

**Characters selected for:**
- Commercial success
- Cultural prevalence
- Analyst familiarity

**NOT selected for:**
- Statistical representativeness
- Proportional IP distribution
- Comprehensive coverage

**Implication:** Findings describe **selected entities** only, not all IP

---

## 3. Temporal Limitations

### 3.1 Snapshot Analysis

**Analysis represents:**
- Datasets as accessed December 2024
- Point-in-time measurement
- Historical web scraping results

**Does NOT reflect:**
- Current dataset versions (may have been updated)
- Current web content (sources may have changed)
- Ongoing curation efforts
- Post-publication modifications

---

### 3.2 Web Source Dynamics

**Original scraping occurred:** 2021-2023 (varies by dataset)  
**Analysis conducted:** December 2024  
**Web sources may have:**
- Been removed or updated
- Changed licensing terms
- Added/removed watermarks
- Modified metadata

**Implication:** Results describe **historical snapshots**, not current web state

---

## 4. Causal Limitations

### 4.1 Cannot Determine Intent

**Cannot establish:**
- Whether dataset creators intended to include copyrighted content
- Whether filtering was attempted or effective
- Whether creators were aware of IP presence
- Whether inclusion violates terms of service
- Whether creators have legal exposure

---

### 4.2 Cannot Determine Effectiveness

**Cannot evaluate:**
- Quality of dataset curation
- Effectiveness of filtering mechanisms
- Adequacy of IP removal efforts
- Success of watermark detection
- Accuracy of NSFW classification

**Why:** No access to:
- Original scraping code
- Filtering algorithms
- Curation decision criteria
- Alternative processing approaches

---

### 4.3 Dataset Differences

**Observed:** Variance in mention rates between datasets (1.14× to 10.81×)

**Cannot determine if caused by:**
- Different web sources scraped
- Different time periods
- Different filtering strategies
- Different curation quality
- Random sampling variation
- Algorithmic differences

**Can only say:** Patterns are **consistent with** varying approaches

---

## 5. Legal Limitations

### 5.1 Not Legal Analysis

**This study does NOT:**
- ❌ Provide legal advice
- ❌ Determine copyright status
- ❌ Establish infringement
- ❌ Evaluate fair use applicability
- ❌ Assess licensing compliance
- ❌ Determine liability
- ❌ Make legal recommendations

---

### 5.2 Requires Legal Expertise

**Questions requiring legal analysis:**
1. Is specific content copyrighted?
2. Does use constitute fair use?
3. Are dataset creators liable?
4. Were terms of service violated?
5. What are legal remedies?
6. How should datasets be curated?
7. What are regulatory implications?

**Answers require:**
- Legal expertise
- Jurisdiction-specific analysis
- Case-by-case evaluation
- Access to licensing agreements
- Understanding of applicable law

**This study provides:** Empirical data that **may inform** legal analysis by domain experts

---

## 6. Technical Limitations

### 6.1 Model Behavior Unknown

**Cannot determine:**
- Whether models trained on these datasets reproduce copyrighted content
- Whether mention frequency correlates with memorization
- Whether character mentions enable generation capabilities
- Whether IP exposure affects model outputs
- How training affects copyright considerations

**Why:** Study examines **datasets** only, not **models**

---

### 6.2 LoRA Context

**Study notes:** 2.45M Batman mentions = 81,738× typical LoRA training requirement (30 images)

**This comparison:**
- ✅ Provides technical context for scale
- ✅ Shows orders-of-magnitude difference
- ❌ Does NOT imply models will reproduce Batman
- ❌ Does NOT establish memorization risk
- ❌ Does NOT determine generation capability

**LoRA fine-tuning differs from base training in:**
- Dataset curation
- Training methodology
- Convergence dynamics
- Alignment procedures
- Architectural differences

---

## 7. Reproducibility Limitations

### 7.1 Dataset Access

**Required for reproduction:**
- Access to original datasets
- Compliance with terms of use
- Multi-TB storage capacity
- Appropriate licensing agreements

**Barriers:**
- Some datasets require registration
- Storage costs substantial
- Bandwidth limitations
- Geographic restrictions possible

---

### 7.2 Computational Resources

**Minimum requirements:**
- 64GB RAM
- Modern multi-core CPU
- 2TB+ storage
- ~48 hours compute time

**Inaccessible to:** Researchers without adequate hardware

---

## 8. Scope Limitations

### 8.1 Excluded Analyses

**This study does NOT examine:**
- NSFW content distribution (separate paper planned)
- Watermark detection patterns (separate paper planned)
- Domain-level analysis (separate paper planned)
- Hate speech or harmful content
- Personally identifiable information
- Demographic representation
- Geographic distribution
- Temporal trends

---

### 8.2 Image Content Not Analyzed

**No analysis of:**
- Visual similarity to source material
- Image quality or resolution
- Photographic composition
- Artistic style
- Visual watermarks
- Embedded logos
- Color patterns
- Metadata tags

**Only text analyzed**

---

## 9. Generalization Limitations

### 9.1 Dataset-Specific

**Findings apply to:**
- COYO-700M
- ReLAION-2B
- DataComp-1B
- As accessed December 2024

**Findings do NOT generalize to:**
- Other datasets
- Future web scraping
- Private datasets
- Curated collections
- Other modalities (audio, video)

---

### 9.2 Character-Specific

**Findings apply to:**
- 48 selected characters
- Major commercial franchises
- English-language mentions

**Findings do NOT generalize to:**
- Other characters
- Independent creators
- Non-franchise IP
- Emerging properties
- Non-commercial work

---

## 10. Ethical Considerations

### 10.1 Potential Misuse

**Study results could be misused to:**
- Make unfounded legal claims
- Misrepresent dataset quality
- Attack dataset creators unfairly
- Overstate IP concerns
- Understate IP concerns

**Responsibility:** Readers must interpret findings carefully and seek domain expertise

---

### 10.2 Dual-Use Nature

**This methodology could be used to:**
- ✅ Improve dataset transparency
- ✅ Inform curation practices
- ✅ Guide policy discussions
- ❌ Attack legitimate research
- ❌ Support frivolous litigation
- ❌ Mischaracterize fair use

---

## Summary

This analysis provides **empirical documentation** of observable textual patterns in dataset caption metadata.

**It does NOT:**
- Analyze images
- Determine copyright
- Establish infringement
- Make legal claims
- Provide comprehensive IP coverage

**Interpretation requires:**
- Legal expertise
- Technical context
- Domain knowledge
- Case-by-case evaluation
- Careful consideration of limitations

**Primary value:**
- Transparency
- Reproducibility
- Baseline for future research
- Context for informed discussion

---

**For questions about limitations:** zero_oversight_project@proton.me
