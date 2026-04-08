# Old Editor System Prompt

Source: `assets/prompts/editor.md` + style guide appended

The old editor loads `load_prompt("editor")` which is `assets/prompts/editor.md`, then appends the full style guide from `assets/prompts/style_editor.md`.

System prompt = `{editor.md}\n\n---\n\n## Reference Style Guide\n\n{style_editor.md}`

See `assets/prompts/editor.md` for the full prompt (145 lines including the Ukraine example).
See `assets/prompts/style_editor.md` for the style guide (395 lines).
