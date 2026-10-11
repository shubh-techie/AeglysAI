# AEGLYSAI-013B — Exact file-change inventory

Base: `0256125`. 71 file moves; 21 additional modified files; 3 added files.

Moves include renamed project directories and project/solution filenames. Namespace, build-path or README edits accompany most moves. Git will infer renames when these changes are staged; no history is rewritten.

## Renamed files

| Original path | Current path |
| --- | --- |
| `benchmarks/AegisAI.Experiments/AegisAI.Experiments.csproj` | `benchmarks/AeglysAI.Experiments/AeglysAI.Experiments.csproj` |
| `benchmarks/AegisAI.Experiments/Experiment.cs` | `benchmarks/AeglysAI.Experiments/Experiment.cs` |
| `benchmarks/AegisAI.Experiments/Program.cs` | `benchmarks/AeglysAI.Experiments/Program.cs` |
| `deployment/docker/AegisAI.DevTools/AegisAI.DevTools.csproj` | `deployment/docker/AeglysAI.DevTools/AeglysAI.DevTools.csproj` |
| `deployment/docker/AegisAI.DevTools/Program.cs` | `deployment/docker/AeglysAI.DevTools/Program.cs` |
| `src/AegisAI.Api/AegisAI.Api.csproj` | `src/AeglysAI.Api/AeglysAI.Api.csproj` |
| `src/AegisAI.Api/Authentication/AuthenticationSetup.cs` | `src/AeglysAI.Api/Authentication/AuthenticationSetup.cs` |
| `src/AegisAI.Api/Authentication/HttpCurrentIdentity.cs` | `src/AeglysAI.Api/Authentication/HttpCurrentIdentity.cs` |
| `src/AegisAI.Api/Authentication/LocalDevelopmentTrust.cs` | `src/AeglysAI.Api/Authentication/LocalDevelopmentTrust.cs` |
| `src/AegisAI.Api/Authorization/AbacConfiguration.cs` | `src/AeglysAI.Api/Authorization/AbacConfiguration.cs` |
| `src/AegisAI.Api/Authorization/AuthorizationEndpoints.cs` | `src/AeglysAI.Api/Authorization/AuthorizationEndpoints.cs` |
| `src/AegisAI.Api/Authorization/RbacConfiguration.cs` | `src/AeglysAI.Api/Authorization/RbacConfiguration.cs` |
| `src/AegisAI.Api/Authorization/RiskConfiguration.cs` | `src/AeglysAI.Api/Authorization/RiskConfiguration.cs` |
| `src/AegisAI.Api/Observability/AuthorizationObservation.cs` | `src/AeglysAI.Api/Observability/AuthorizationObservation.cs` |
| `src/AegisAI.Api/Observability/LoggingAuthorizationAuditSink.cs` | `src/AeglysAI.Api/Observability/LoggingAuthorizationAuditSink.cs` |
| `src/AegisAI.Api/Program.cs` | `src/AeglysAI.Api/Program.cs` |
| `src/AegisAI.Api/appsettings.example.json` | `src/AeglysAI.Api/appsettings.example.json` |
| `src/AegisAI.Application/AegisAI.Application.csproj` | `src/AeglysAI.Application/AeglysAI.Application.csproj` |
| `src/AegisAI.Application/Authorization/AbacContext.cs` | `src/AeglysAI.Application/Authorization/AbacContext.cs` |
| `src/AegisAI.Application/Authorization/AbacEvaluator.cs` | `src/AeglysAI.Application/Authorization/AbacEvaluator.cs` |
| `src/AegisAI.Application/Authorization/AuthorizationDecision.cs` | `src/AeglysAI.Application/Authorization/AuthorizationDecision.cs` |
| `src/AegisAI.Application/Authorization/AuthorizationRequest.cs` | `src/AeglysAI.Application/Authorization/AuthorizationRequest.cs` |
| `src/AegisAI.Application/Authorization/ContextualRiskEngine.cs` | `src/AeglysAI.Application/Authorization/ContextualRiskEngine.cs` |
| `src/AegisAI.Application/Authorization/IAbacEvaluator.cs` | `src/AeglysAI.Application/Authorization/IAbacEvaluator.cs` |
| `src/AegisAI.Application/Authorization/IAuthorizationEngine.cs` | `src/AeglysAI.Application/Authorization/IAuthorizationEngine.cs` |
| `src/AegisAI.Application/Authorization/IRbacPolicyProvider.cs` | `src/AeglysAI.Application/Authorization/IRbacPolicyProvider.cs` |
| `src/AegisAI.Application/Authorization/ModelBAuthorizationEngine.cs` | `src/AeglysAI.Application/Authorization/ModelBAuthorizationEngine.cs` |
| `src/AegisAI.Application/Authorization/ModelCAuthorizationEngine.cs` | `src/AeglysAI.Application/Authorization/ModelCAuthorizationEngine.cs` |
| `src/AegisAI.Application/Authorization/RbacAuthorizationEngine.cs` | `src/AeglysAI.Application/Authorization/RbacAuthorizationEngine.cs` |
| `src/AegisAI.Application/Authorization/RbacPolicy.cs` | `src/AeglysAI.Application/Authorization/RbacPolicy.cs` |
| `src/AegisAI.Application/Identity/AuthenticatedIdentity.cs` | `src/AeglysAI.Application/Identity/AuthenticatedIdentity.cs` |
| `src/AegisAI.Application/Identity/ICurrentIdentity.cs` | `src/AeglysAI.Application/Identity/ICurrentIdentity.cs` |
| `src/AegisAI.Application/Observability/AuthorizationAuditEvent.cs` | `src/AeglysAI.Application/Observability/AuthorizationAuditEvent.cs` |
| `src/AegisAI.Domain/AegisAI.Domain.csproj` | `src/AeglysAI.Domain/AeglysAI.Domain.csproj` |
| `src/AegisAI.Domain/Authorization/AbacRule.cs` | `src/AeglysAI.Domain/Authorization/AbacRule.cs` |
| `src/AegisAI.Domain/Authorization/Action.cs` | `src/AeglysAI.Domain/Authorization/Action.cs` |
| `src/AegisAI.Domain/Authorization/AttributeCondition.cs` | `src/AeglysAI.Domain/Authorization/AttributeCondition.cs` |
| `src/AegisAI.Domain/Authorization/AttributeSet.cs` | `src/AeglysAI.Domain/Authorization/AttributeSet.cs` |
| `src/AegisAI.Domain/Authorization/Permission.cs` | `src/AeglysAI.Domain/Authorization/Permission.cs` |
| `src/AegisAI.Domain/Authorization/Resource.cs` | `src/AeglysAI.Domain/Authorization/Resource.cs` |
| `src/AegisAI.Domain/Authorization/RiskContext.cs` | `src/AeglysAI.Domain/Authorization/RiskContext.cs` |
| `src/AegisAI.Domain/Authorization/Role.cs` | `src/AeglysAI.Domain/Authorization/Role.cs` |
| `src/AegisAI.Domain/Authorization/Subject.cs` | `src/AeglysAI.Domain/Authorization/Subject.cs` |
| `src/AegisAI.Infrastructure/AegisAI.Infrastructure.csproj` | `src/AeglysAI.Infrastructure/AeglysAI.Infrastructure.csproj` |
| `src/AegisAI.Infrastructure/Authorization/InMemoryAbacContextProvider.cs` | `src/AeglysAI.Infrastructure/Authorization/InMemoryAbacContextProvider.cs` |
| `src/AegisAI.Infrastructure/Authorization/InMemoryRbacPolicyProvider.cs` | `src/AeglysAI.Infrastructure/Authorization/InMemoryRbacPolicyProvider.cs` |
| `src/AegisAI.Infrastructure/Authorization/InMemoryRiskContextProvider.cs` | `src/AeglysAI.Infrastructure/Authorization/InMemoryRiskContextProvider.cs` |
| `tests/AegisAI.Application.Tests/AbacEvaluationTests.cs` | `tests/AeglysAI.Application.Tests/AbacEvaluationTests.cs` |
| `tests/AegisAI.Application.Tests/AegisAI.Application.Tests.csproj` | `tests/AeglysAI.Application.Tests/AeglysAI.Application.Tests.csproj` |
| `tests/AegisAI.Application.Tests/AuthenticatedIdentityTests.cs` | `tests/AeglysAI.Application.Tests/AuthenticatedIdentityTests.cs` |
| `tests/AegisAI.Application.Tests/ContextualRiskTests.cs` | `tests/AeglysAI.Application.Tests/ContextualRiskTests.cs` |
| `tests/AegisAI.Application.Tests/README.md` | `tests/AeglysAI.Application.Tests/README.md` |
| `tests/AegisAI.Application.Tests/RbacAuthorizationTests.cs` | `tests/AeglysAI.Application.Tests/RbacAuthorizationTests.cs` |
| `tests/AegisAI.ArchitectureTests/AegisAI.ArchitectureTests.csproj` | `tests/AeglysAI.ArchitectureTests/AeglysAI.ArchitectureTests.csproj` |
| `tests/AegisAI.ArchitectureTests/ProjectDependencyTests.cs` | `tests/AeglysAI.ArchitectureTests/ProjectDependencyTests.cs` |
| `tests/AegisAI.Domain.Tests/AegisAI.Domain.Tests.csproj` | `tests/AeglysAI.Domain.Tests/AeglysAI.Domain.Tests.csproj` |
| `tests/AegisAI.Domain.Tests/AttributePolicyTests.cs` | `tests/AeglysAI.Domain.Tests/AttributePolicyTests.cs` |
| `tests/AegisAI.Domain.Tests/AuthorizationConceptTests.cs` | `tests/AeglysAI.Domain.Tests/AuthorizationConceptTests.cs` |
| `tests/AegisAI.Domain.Tests/README.md` | `tests/AeglysAI.Domain.Tests/README.md` |
| `tests/AegisAI.Domain.Tests/RiskContextTests.cs` | `tests/AeglysAI.Domain.Tests/RiskContextTests.cs` |
| `tests/AegisAI.Experiments.Tests/AegisAI.Experiments.Tests.csproj` | `tests/AeglysAI.Experiments.Tests/AeglysAI.Experiments.Tests.csproj` |
| `tests/AegisAI.Experiments.Tests/ExperimentTests.cs` | `tests/AeglysAI.Experiments.Tests/ExperimentTests.cs` |
| `tests/AegisAI.IntegrationTests/AegisAI.IntegrationTests.csproj` | `tests/AeglysAI.IntegrationTests/AeglysAI.IntegrationTests.csproj` |
| `tests/AegisAI.IntegrationTests/AuthenticationTests.cs` | `tests/AeglysAI.IntegrationTests/AuthenticationTests.cs` |
| `tests/AegisAI.IntegrationTests/AuthorizationAuditTests.cs` | `tests/AeglysAI.IntegrationTests/AuthorizationAuditTests.cs` |
| `tests/AegisAI.IntegrationTests/AuthorizationEndpointTests.cs` | `tests/AeglysAI.IntegrationTests/AuthorizationEndpointTests.cs` |
| `tests/AegisAI.IntegrationTests/HealthEndpointTests.cs` | `tests/AeglysAI.IntegrationTests/HealthEndpointTests.cs` |
| `tests/AegisAI.IntegrationTests/LocalDevelopmentTrustTests.cs` | `tests/AeglysAI.IntegrationTests/LocalDevelopmentTrustTests.cs` |
| `tests/AegisAI.IntegrationTests/ModelBEndpointTests.cs` | `tests/AeglysAI.IntegrationTests/ModelBEndpointTests.cs` |
| `tests/AegisAI.IntegrationTests/ModelCEndpointTests.cs` | `tests/AeglysAI.IntegrationTests/ModelCEndpointTests.cs` |
| `AegisAI.sln` | `AeglysAI.sln` |

## Additional modified files

- `.github/workflows/ci.yml`
- `.github/workflows/security.yml`
- `.gitleaks.toml`
- `AGENTS.md`
- `README.md`
- `deployment/docker/Dockerfile`
- `deployment/docker/compose.yaml`
- `dev`
- `docs/aegisai/DEVELOPMENT_LOG.md`
- `docs/aegisai/RESEARCH_SCOPE.md`
- `docs/aegisai/TARGET_ARCHITECTURE.md`
- `docs/aegisai/architecture/RESEARCH_ARCHITECTURE.md`
- `docs/aegisai/architecture/SYSTEM_ARCHITECTURE.md`
- `docs/aegisai/research/CLAIMS_REGISTER.md`
- `docs/aegisai/research/RESEARCH_MODELS.md`
- `docs/aegisai/threat-model/THREAT_MODEL_V1.md`
- `research/README.md`
- `scripts/security/README.md`
- `scripts/security/scan.py`
- `scripts/security/tests/check_docker_context.py`
- `scripts/security/tests/test_scan.py`

## Added files

- `docs/aeglysai/AEGLYSAI-013B-NAMING-MIGRATION.md`
- `docs/aeglysai/AEGLYSAI-013B-FILE-CHANGES.md`
- `scripts/tests/test_compose_compatibility.py`

Generated old bin/obj outputs were cleaned locally and are not tracked changes. Frozen research artifacts, historical snapshots, private originals, tags and remote configuration are excluded from this change.
