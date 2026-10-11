namespace AeglysAI.Domain.Authorization;

public sealed record Action
{
    public string Name { get; }

    public Action(string value)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(value);
        Name = value;
    }
}
