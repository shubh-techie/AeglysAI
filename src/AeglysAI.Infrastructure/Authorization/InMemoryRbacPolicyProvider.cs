using AeglysAI.Application.Authorization;

namespace AeglysAI.Infrastructure.Authorization;

public sealed class InMemoryRbacPolicyProvider : IRbacPolicyProvider
{
    private readonly RbacPolicy _policy;

    public InMemoryRbacPolicyProvider(RbacPolicy policy)
    {
        ArgumentNullException.ThrowIfNull(policy);
        _policy = policy;
    }

    public RbacPolicy GetPolicy() => _policy;
}
