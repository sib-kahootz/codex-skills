# pull-request

Prepares, reviews, updates, pushes, and creates GitHub pull requests from local branch work, defaulting to draft PRs unless requested otherwise.

## Optional tag configuration

The skill does not add, remove, or propose tags unless `references/tags.local.json` is present and valid. This ignored local file lets each organisation define its own tags without making the skill organisation-specific.

Create the file with a JSON object containing a `tags` array. Each entry needs a tag name, category, and short meaning:

```json
{
  "tags": [
    {
      "tag": "bug",
      "category": "change-type",
      "meaning": "Fixes a defect."
    }
  ]
}
```

Add only tags that exist in the target repository. Keep the file local: it is ignored by Git and must not be committed. GitHub CLI uses the term `label` in its commands; the skill maps configured tags to those command arguments.
