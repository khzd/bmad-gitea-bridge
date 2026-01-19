# Story-001: Patient Account Creation

## User Story

**As a** patient  
**I want to** create an account on the patient portal  
**So that** I can access my medical records online

## Description

New patients need a simple, secure way to create an account and verify their identity to access the portal.

## Epic

Epic-001: Patient Portal - Medical Records Access

## Acceptance Criteria

### Functional
- [ ] Patient can enter email, password, and basic info (name, DOB, health card number)
- [ ] System validates health card number against EHR database
- [ ] System sends verification email with unique token
- [ ] Patient can click email link to verify account
- [ ] Account activation requires 2FA setup (SMS or authenticator app)
- [ ] Failed verification attempts are logged and rate-limited

### Non-Functional
- [ ] Password must meet complexity requirements (12+ chars, mixed case, numbers, symbols)
- [ ] Account creation completes in <5 seconds
- [ ] Responsive design works on mobile/tablet/desktop
- [ ] French language support available

## Tasks

- [ ] Design account creation form (UX Designer)
- [ ] Implement frontend form validation (Dev)
- [ ] Create backend API endpoint /api/register (Dev)
- [ ] Integrate with EHR patient lookup service (Dev)
- [ ] Implement email verification service (Dev)
- [ ] Add 2FA setup flow (Dev)
- [ ] Write unit tests for validation logic (TEA)
- [ ] Write integration tests for registration flow (TEA)
- [ ] Security review and penetration testing (Architect)
- [ ] HIPAA compliance documentation (Tech Writer)

## Technical Notes

### API Endpoint
```
POST /api/v1/auth/register
{
  "email": "patient@example.com",
  "password": "SecurePass123!",
  "firstName": "Jane",
  "lastName": "Doe",
  "dateOfBirth": "1985-03-15",
  "healthCardNumber": "1234-567-890"
}
```

### Security Requirements
- bcrypt password hashing (cost factor 12)
- Rate limiting: 5 attempts per IP per hour
- Email verification token expires in 24 hours
- All PII encrypted at rest using AES-256

## Dependencies

- EHR patient lookup API ready
- Email service configured (SendGrid)
- 2FA library integrated (Google Authenticator compatible)

## Definition of Done

- [ ] Code reviewed and approved
- [ ] All tests passing (unit + integration)
- [ ] Security review completed
- [ ] Deployed to staging environment
- [ ] QA sign-off
- [ ] Documentation updated
- [ ] Demo to stakeholders completed

## Story Points

**8 points** (Fibonacci scale)

## Assignee

**Dev** (Amelia)

## Status

**Todo**

## Priority

**High**

## Labels

`authentication`, `security`, `epic-001`, `patient-portal`

---

**Created**: 2026-01-15  
**Last Updated**: 2026-01-19  
**Sprint**: Sprint 5
