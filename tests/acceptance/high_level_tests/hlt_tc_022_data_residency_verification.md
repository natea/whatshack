# HLT-TC-022: Data Residency Verification (af-south-1)

**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Assistant (Claude)

## 1. Test Overview
This HLT verifies that Township Connect's data is stored in the appropriate geographic region (af-south-1, AWS Cape Town region) to comply with POPIA's data residency requirements, ensuring that South African users' personal information remains within South African borders.

## 2. User Story / Scenario
* **Feature (PRD 2.3):** Achieve 100% POPIA compliance, including data residency requirements.
* **Scenario (HLT Strategy 4.5):** Verify data residency. Confirm that Supabase instance is configured for `af-south-1` and data is stored there.

## 3. Preconditions
* Township Connect's Supabase instance is set up and operational.
* Administrative access to the Supabase dashboard or configuration is available.
* If direct dashboard access is not available, API or CLI tools that can query instance metadata are accessible.

## 4. Test Steps

| Step | Admin/Verification Action | Expected Result |
|------|---------------------------|-----------------|
| 1 | Access the Supabase dashboard for the Township Connect project | Dashboard is accessible and shows the project details. |
| 2 | Navigate to the project settings or infrastructure information section | Settings page displays information about the hosting configuration. |
| 3 | Verify the AWS region setting for the Supabase instance | The region is explicitly set to `af-south-1` (AWS Cape Town region). |
| 4 | Verify that database backups and replicas (if any) are also configured to remain within the `af-south-1` region | All backup and replication configurations specify the `af-south-1` region. |
| 5 | If available, check the actual physical server location through infrastructure logs or metadata | Server location is confirmed to be in Cape Town, South Africa. |
| 6 | Verify that any additional services connected to Supabase (e.g., storage for files) are also hosted in the `af-south-1` region | All connected services are configured to use the `af-south-1` region. |
| 7 | Check any data transfer configurations to ensure data doesn't leave the region during processing | No cross-region data transfer configurations are present that would move data outside of South Africa. |
| 8 | Review the Supabase service agreement or documentation to confirm their compliance with South African data residency requirements | Documentation confirms compliance with South African data residency requirements. |
| 9 | If possible, perform a network trace or latency test from a South African location to verify proximity of the server | Network latency is consistent with a South African server location rather than international locations. |

## 5. Acceptance Criteria (AI Verifiable)
* The Supabase instance hosting Township Connect's data is definitively configured to use the `af-south-1` (Cape Town) AWS region.
* All database storage, including backups and replicas, is contained within the `af-south-1` region.
* Any additional services or integrations that process Township Connect user data are also hosted within South Africa.
* There are no configurations or processes that would routinely transfer personal data outside of South Africa.
* The implementation complies with POPIA requirements for data residency.
* Documentation or service agreements explicitly confirm the data residency commitment.

## 6. References
* PRD Section 2.3: Specific Objectives - 100% POPIA compliance
* High-Level Test Strategy Report Section 4.5: POPIA Compliance
* Master Acceptance Test Plan Section 3, Phase 5: POPIA Compliance Verification
* Protection of Personal Information Act (POPIA) requirements for data residency
* Supabase documentation on regional deployment options
* AWS documentation on the af-south-1 (Cape Town) region

## 7. Notes
* This test focuses specifically on the geographic location of data storage, which is a key requirement for POPIA compliance.
* For AI verification purposes, screenshots or exports of configuration settings can be analyzed to confirm the region setting.
* While this test primarily verifies configuration rather than functionality, it is critical for legal compliance.
* In some cases, direct verification may require administrative access to Supabase or AWS, which might need to be performed by authorized personnel.
* If direct verification is not possible, indirect methods such as:
  * Reviewing signed attestations from the hosting provider
  * Checking service agreements that specify data residency
  * Analyzing network routing and latency patterns
  * May be used as alternative verification approaches.
* This test should be repeated periodically (e.g., quarterly) to ensure ongoing compliance, especially after any infrastructure changes.