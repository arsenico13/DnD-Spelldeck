set nocompatible
syntax on
filetype plugin indent on

" Basic Markdown support
autocmd BufRead,BufNewFile *.md set filetype=markdown
autocmd FileType markdown setlocal wrap linebreak spell spelllang=it,en
