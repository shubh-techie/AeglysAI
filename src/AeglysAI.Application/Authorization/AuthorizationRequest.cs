using AeglysAI.Domain.Authorization;
using ResourceAction = AeglysAI.Domain.Authorization.Action;

namespace AeglysAI.Application.Authorization;

public sealed record AuthorizationRequest
{
    public Subject Subject { get; }
    public Resource Resource { get; }
    public ResourceAction Action { get; }

    public AuthorizationRequest(Subject subject, Resource resource, ResourceAction action)
    {
        ArgumentNullException.ThrowIfNull(subject);
        ArgumentNullException.ThrowIfNull(resource);
        ArgumentNullException.ThrowIfNull(action);
        Subject = subject;
        Resource = resource;
        Action = action;
    }
}
