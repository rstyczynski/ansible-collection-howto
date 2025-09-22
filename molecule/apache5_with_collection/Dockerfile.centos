FROM quay.io/centos/centos:stream9

RUN dnf -y update && \
    dnf -y install \
      systemd systemd-udev dbus \
      python3 python3-pip  \
      sudo && \
    dnf clean all && rm -rf /var/cache/dnf