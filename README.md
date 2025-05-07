A simple demo of how to use AI from a Python script.
It requires an OpenRouter API key stored in the `~/.openrouter.key` file. You can obtain one after registering at https://openrouter.ai/.

This is the vim shortcut I use to proofread selected text:

```
nnoremap <leader>P :%!ai-processor.py --task=proofread<CR>
vnoremap <leader>P :!ai-processor.py --task=proofread<CR>
```

And this one is for translation:

```
nnoremap <leader>T :%!ai-processor.py --task=translate<CR>
vnoremap <leader>T :!ai-processor.py --task=translate<CR>
```
