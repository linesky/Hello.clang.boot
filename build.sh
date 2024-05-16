printf "\x1bc\x1b[43;37m give me a .c file to compile\n"
read ai
rm /tmp/*.com
rm /tmp/*.bin
nasm -o /tmp/boot.bin boot.asm
gcc -o3 -c "$ai" -o /tmp/kernel.o -nostdlib
ld -T link.ld /tmp/kernel.o -o /tmp/hello.com -nostdlib
objcopy -O binary  /tmp/hello.com  /tmp/hellos.c32
dd if=/dev/zero of=new.img bs=1024 count=1440
chmod 777 new.img
chmod 777 /tmp/*.com
chmod 777 /tmp/*.bin
sudo mkfs.vfat -n 'BOOT' -S 512 -f 2 -F 12 "new.img"
chmod 777 new.img
sudo mkdir /mnt/new
mount -t vfat -o loop "new.img" "/mnt/new"
chmod 777 /mnt/new/*.com
cp /tmp/hellos.c32 "/mnt/new/#.c32"
umount /mnt/new
echo "wait..."
chmod 777 new.img
sleep 2
sudo dd if=/tmp/boot.bin of=/tmp/new.img bs=512 count=1 conv=notrunc

