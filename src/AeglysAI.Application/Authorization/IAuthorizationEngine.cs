namespace AeglysAI.Application.Authorization;

public interface IAuthorizationEngine
{
    AuthorizationDecision Authorize(AuthorizationRequest request);
}
