# default
alias psgrep="ps aux | egrep -i $1" # process search
alias hh="history | egrep -i" # search in history
alias upd="sudo apt update && sudo apt full-upgrade -y && sudo apt dist-upgrade -y" # update system to latest packages in release

# grc colored
alias cvs="grc --colour=auto cvs"
alias diff="grc --colour=auto diff"
alias esperanto="grc --colour=auto esperanto"
alias gcc="grc --colour=auto gcc"
alias irclog="grc --colour=auto irclog"
alias ldap="grc --colour=auto ldap"
alias log="grc --colour=auto log"
alias netstat="grc --colour=auto netstat"
alias ping="grc --colour=auto ping"
alias proftpd="grc --colour=auto proftpd"
alias traceroute="grc --colour=auto traceroute"
alias wdiff="grc --colour=auto wdiff"
alias make="grc --colour=auto make"
alias ll="grc --colour=auto ls -laFh --color=always"
alias l = "grc --colour=auto ls -lah --color=always"

# admin tooling
alias tcp="netstat -ltupn" # list open tcp port without sudo
alias port="sudo ss -altp" # list open tcp port with process name/PID

# docker
alias dockupd="docker-compose stop && docker-compose rm && docker-compose pull && docker-compose up -d" # restart & update service from docker-compose.yml config in current dir
alias dcupd="dockupd" # short alias
alias dc="docker-compose"
alias dcl="docker-compose logs -f"
alias dcr="docker-compose stop && docker-compose up -d"
alias n='nvim'
