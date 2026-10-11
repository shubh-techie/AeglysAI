# Beginner quick start

You can contribute documentation or tests without knowing advanced machine learning.
Read [CONTRIBUTING](../../CONTRIBUTING.md), conduct and disclosure guidance first.
Choose a small issue with a clear goal; ask the maintainer to agree on scope before
starting. No production credentials or cloud account is required.

For .NET changes, install the .NET 8 SDK, clone the official repository, open
AeglysAI.sln and run:

```sh
dotnet restore AeglysAI.sln
dotnet build AeglysAI.sln -c Release --no-restore
dotnet test AeglysAI.sln -c Release --no-build --no-restore
```

For evidence/contract changes, create an isolated Python environment, install
scripts/community/requirements.txt and run the community tests described in the
[evidence standard](../evidence/README.md). Documentation changes require local
link and diff checks; do not install unrelated toolchains.

Make one focused change on a local branch. Add a meaningful test, report commands
actually run and review filenames/diffs with the security gates before requesting
review. Existing history findings are not your fault and must not be hidden to
get a passing check. Do not push until owner publication approval is available.
Recognition is opt-in; declining it does not affect contribution review.
