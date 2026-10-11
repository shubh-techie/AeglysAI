namespace AeglysAI.Application.Authorization;

public interface IRbacPolicyProvider
{
    RbacPolicy GetPolicy();
}
