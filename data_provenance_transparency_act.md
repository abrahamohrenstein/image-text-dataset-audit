### **Data Provenance Transparency Act of 2026**

**Short Title**

This Act may be cited as the "Data Provenance Transparency Act of 2026."

---

### **Section 1 – Findings and Purpose**

**(a) Findings**

Congress finds that:

1. **Scale of Use**: Commercial generative artificial intelligence systems are trained on datasets containing billions of images, text documents, audio files, and other copyrighted works, the provenance of which is rarely disclosed to users or rights holders.

2. **Consumer Protection Gap**: Consumers, businesses, and creative professionals who rely on AI-generated outputs for commercial purposes lack standardized information about:
   - Whether training data was legally licensed or consensually provided
   - The risk of copyright liability arising from AI-generated outputs
   - Whether the AI provider offers legal indemnification

3. **Market Failure**: Voluntary disclosure efforts by AI developers have proven inconsistent, non-standardized, and insufficient to enable informed consumer choice or effective oversight.

4. **Existing Precedent**: Federal law already requires disclosure of product ingredients (Federal Food, Drug, and Cosmetic Act), energy efficiency (Energy Policy and Conservation Act), and content ratings (voluntary ESRB system backed by FTC enforcement). Data provenance labeling extends these consumer-protection principles to AI-generated content.

**(b) Purpose**

The purpose of this Act is to:

1. Establish a standardized, mandatory disclosure system for the data provenance of commercial generative AI systems
2. Enable consumers and businesses to make informed decisions about AI services based on legal and ethical sourcing practices
3. Create market incentives for AI developers to prioritize licensed, consented, and legally compliant training data
4. Reduce copyright infringement risk for end users of AI-generated content

---

### **Section 2 – Definitions**

For purposes of this Act:

**(a) Commercial Generative AI System**: Any artificial intelligence system or service that:
1. Generates text, images, audio, video, code, or other creative outputs in response to user prompts
2. Is offered for commercial purposes (including subscription services, API access, or advertising-supported platforms)
3. Has been trained on a dataset exceeding 1 million data points

**(b) Provenance**: The documented origin, licensing status, and legal authorization for each element of a training dataset, including:
1. Public domain materials
2. Licensed copyrighted works (with documented permission)
3. User-contributed content with explicit opt-in consent
4. Materials of disputed or unverified legal status

**(c) Accredited Auditor**: An independent third-party organization certified by the National Institute of Standards and Technology (NIST) to verify data provenance claims according to standards established under Section 5.

---

### **Section 3 – Mandatory Data Provenance Label**

**(a) Display Requirement**

Every commercial generative AI system offered to users in the United States shall display a standardized Data Provenance Label on:
1. The primary user interface where outputs are generated
2. All API documentation and developer portals
3. Marketing materials and terms of service

**(b) Label Contents**

The Data Provenance Label shall contain the following three elements:

**Element 1: Provenance Grade**

A single-letter grade (A through F) indicating the percentage of the training dataset that consists of:
- Licensed copyrighted works with documented authorization
- Public domain materials
- User-contributed content with explicit, informed consent

| Grade | Percentage Licensed/Consented/Public Domain | Display Color |
|-------|---------------------------------------------|---------------|
| A | 95–100% | Green |
| B | 85–94.9% | Light Green |
| C | 70–84.9% | Yellow |
| D | 50–69.9% | Orange |
| F | Below 50% OR provenance unknown/unverified | Red |

**Element 2: Independent Audit Status**

The percentage of the training dataset that has been verified by an Accredited Auditor, displayed as:
- "X% Independently Verified" (where X is the audited percentage)
- After January 1, 2029: Models with less than 80% verification automatically receive Grade F

**Element 3: Copyright Indemnification**

A clear statement of whether the provider offers commercial users indemnification against copyright infringement claims arising from AI-generated outputs:
- "Full Indemnity Provided" (provider assumes liability)
- "No Indemnity" (user assumes liability)
- "Partial Indemnity" (with link to specific terms)

**(c) Technical Specifications**

The label must:
1. Be prominently displayed and visible before any output is generated
2. Be machine-readable (structured data format for accessibility)
3. Link to a detailed Provenance Report containing:
   - Dataset composition by source category
   - Methodology for determining provenance
   - Date of last audit
   - Contact information for rights holders to request exclusion

**(d) Safe Harbor for Good-Faith Compliance**

Providers who:
1. Engage an Accredited Auditor within 180 days of this Act's effective date
2. Display interim grades based on good-faith self-assessment
3. Update labels within 30 days of audit completion

...shall not be subject to penalties under Section 4 during the transition period specified in Section 6.

---

### **Section 4 – Enforcement**

**(a) Federal Trade Commission Authority**

The Federal Trade Commission (FTC) shall have primary enforcement authority for this Act. The FTC may:
1. Conduct investigations of label accuracy
2. Require production of training dataset documentation
3. Issue cease-and-desist orders for non-compliance
4. Assess civil penalties as specified in subsection (b)

**(b) Penalties**

1. **Initial Violation**: Written warning and 90-day cure period
2. **Knowing Misrepresentation**: Civil penalty of $50,000 per day of violation
3. **Pattern of Deception**: Up to $500,000 per violation, plus disgorgement of profits obtained during the period of deceptive labeling

**(c) Whistleblower Provisions**

The FTC shall establish a confidential reporting mechanism for:
1. Employees of AI companies to report label inaccuracies
2. Rights holders to report unauthorized use of their works in training data
3. Independent researchers to submit evidence of label violations

Whistleblowers whose information leads to successful enforcement actions shall be eligible for rewards of 10–30% of collected penalties, up to $1 million.

**(d) Private Right of Action (Limited)**

Copyright holders may bring civil actions against providers who:
1. Display a Grade A or B label while knowingly including the plaintiff's copyrighted work without authorization
2. Fail to remove plaintiff's work from training data after receiving formal notice under subsection (e)

**(e) Opt-Out Mechanism**

Within 180 days of enactment, the FTC shall establish a centralized registry where copyright holders may:
1. Submit lists of works to be excluded from AI training
2. Verify whether their works are included in audited datasets
3. Request removal from future training cycles

AI providers must check this registry before each new training run and exclude all listed works.

---

### **Section 5 – Accreditation and Standards**

**(a) NIST Responsibilities**

Within 180 days of enactment, the National Institute of Standards and Technology (NIST) shall:

1. Establish technical standards for data provenance auditing, including:
   - Sampling methodologies for large datasets
   - Documentation requirements for licensing claims
   - Procedures for verifying consent mechanisms

2. Create an accreditation program for independent auditors, requiring:
   - Technical expertise in AI training processes
   - Independence from AI providers (no financial conflicts)
   - Liability insurance of at least $5 million

3. Publish a public registry of Accredited Auditors

**(b) Audit Methodology**

Accredited Auditors must:
1. Use statistically representative sampling for datasets exceeding 100 million elements
2. Verify licensing documentation for at least 10,000 randomly selected training elements
3. Interview data-sourcing personnel under oath
4. Issue public reports summarizing findings (without disclosing trade secrets)

**(c) Costs**

Audit costs shall be borne by the AI provider requesting certification. NIST may establish a cost-sharing program for small businesses and open-source projects.


**(d) - Use of Accredited Auditors**

1. Certification Program: Within 180 days of enactment, NIST shall establish a certification program for existing data cleaning and verification companies to become Accredited Auditors.
2. Eligibility Requirements:

  - ISO 27001 or equivalent security certification
  - GDPR compliance infrastructure
  - Demonstrated capacity to audit datasets >100M records
  - No financial relationship with AI companies being audited

3. Government Contracts: NIST may award contracts to Accredited Auditors to conduct audits of datasets used in federally-funded AI research.
4. Private Sector Use: Commercial AI companies may hire any Accredited Auditor; NIST maintains public registry of certified entities.

---

### **Section 6 – Transition Period and Effective Date**

**(a) Effective Date**: This Act takes effect 12 months after enactment.

**(b) Transition Period**: AI systems deployed before the effective date shall have 24 months to:
1. Complete initial audits
2. Update labels to reflect verified provenance
3. Implement opt-out mechanisms

During this transition period, providers may display Grade D ("In Transition") if they demonstrate good-faith progress toward compliance.

**(c) New Systems**: AI systems launched after the effective date must display compliant labels at launch.

---

### **Section 7 – Preemption and Relationship to Other Laws**

**(a) Federal Floor**: This Act establishes a federal minimum standard. States may impose additional transparency requirements that are more stringent.

**(b) No Diminishment of Copyright Law**: Nothing in this Act shall be construed to:
1. Create new fair use defenses for unauthorized use of copyrighted works in AI training
2. Limit remedies available under existing copyright law (17 U.S.C. § 101 et seq.)
3. Preempt state laws protecting publicity rights or privacy

**(c) International Harmonization**: The Secretary of Commerce, in consultation with the U.S. Trade Representative, shall pursue international agreements to harmonize data provenance standards with trading partners.

---

### **Section 8 – Severability**

If any provision of this Act, or its application to any person or circumstance, is held invalid, the remainder of the Act and its application to other persons or circumstances shall not be affected.

---

## **APPENDIX: Sample Labels** (For Illustrative Purposes)

### **Example 1: Fully Licensed Model** (e.g., Adobe Firefly, Getty AI)
```
┌─────────────────────────────────────┐
│ DATA PROVENANCE LABEL               │
├─────────────────────────────────────┤
│ Grade: A (98% Licensed/Consented)   │
│ Audit Status: 100% Verified         │
│ Indemnity: Full Indemnity Provided  │
│ [Click for Detailed Report]         │
└─────────────────────────────────────┘
```

### **Example 2: LAION-Derived Model** (e.g., Stable Diffusion 1.x era)
```
┌─────────────────────────────────────┐
│ DATA PROVENANCE LABEL               │
├─────────────────────────────────────┤
│ Grade: F (<5% Licensed/Consented)   │
│ Audit Status: 0% Verified           │
│ Indemnity: No Indemnity             │
│ [Click for Detailed Report]         │
└─────────────────────────────────────┘
```

### **Example 3: Transitional Compliance**
```
┌─────────────────────────────────────┐
│ DATA PROVENANCE LABEL               │
├─────────────────────────────────────┤
│ Grade: D (In Transition)            │
│ Audit Status: 35% Verified          │
│ Indemnity: Under Review             │
│ [Audit Expected: Q2 2027]           │
└─────────────────────────────────────┘
```

---

