\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{scirep}[2019/11/19]

\LoadClass[11pt]{article}
\RequirePackage[utf8]{inputenc}
\RequirePackage[czech]{babel}

\RequirePackage[margin=3cm]{geometry}
\RequirePackage{fancyhdr}
\RequirePackage[decimalsymbol=comma]{siunitx}
\RequirePackage{float}
%\RequirePackage{subfiles}
\RequirePackage{graphicx}
%\RequirePackage{pgfplotstable}
\RequirePackage{booktabs}
\RequirePackage{verbatim}
\RequirePackage{amsmath}
\RequirePackage[hidelinks=true]{hyperref}
\RequirePackage{icomma}
\RequirePackage{siunitx}
%\RequirePackage[]{xcolor}
\RequirePackage{wrapfig}
\RequirePackage{caption}
\RequirePackage{lipsum}
\RequirePackage{chemformula}

\captionsetup[figure]{skip=0pt}

\RequirePackage{etoolbox}
\preto\tabular{\shorthandoff{-}}

\setlength{\headheight}{14pt}

\pagestyle{fancy}
\fancyhead{}
\parindent 2ex
%\setlength{\parskip}{\baselineskip}
\graphicspath{{plots/}{./}{figures/}{../plots/}{../figures/}}

\newcommand{\leftheader}[1]{\fancyhead[L]{#1}}
\newcommand{\centerheader}[1]{\fancyhead[C]{#1}}
\newcommand{\rightheader}[1]{\fancyhead[R]{#1}}

\newcommand{\cz}[1]{\textit{#1}}

\sisetup{separate-uncertainty=true}