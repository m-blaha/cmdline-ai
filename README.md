A simple demo of how to use AI from a Python script.

This is the vim shortcut I use to proofread selected text:
nnoremap <leader>P :%!ai-processor.py --task=proofread<CR>
vnoremap <leader>P :!ai-processor.py --task=proofread<CR>

And this one is for translation:
nnoremap <leader>T :%!ai-processor.py --task=translate<CR>
vnoremap <leader>T :!ai-processor.py --task=translate<CR>
