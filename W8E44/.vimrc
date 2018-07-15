set nocompatible              " be iMproved, required
filetype off                  " required

set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Bundle 'scrooloose/nerdtree'

call vundle#end()            " required
filetype plugin indent on    " required

syntax on 
set incsearch
set ignorecase
set hlsearch
set smartcase

set fileencodings=utf-8,gb2312,gbk,gb18030
set termencoding=utf-8
set encoding=prc

set expandtab

set tabstop=4

set shiftwidth=4

set showmatch

let mapleader=';'

set autoindent

set smartindent

set hlsearch

set ruler
set number
set nocompatible
set backspace=indent,eol,start
set backspace=2

set ignorecase

let NERDTreeShowHidden=0
let NERDTreeIgnore = ['\.pyc$', '__pycache__']
let g:NERDTreeWinSize=35
map <leader>nn :NERDTreeToggle<cr>
map <leader>nb :NERDTreeFromBookmark<Space>
map <leader>nf :NERDTreeFind<cr>


