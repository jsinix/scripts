#!/usr/bin/perl -w

# Disclaimer: This script is only for educational purposes.
# Please use this at your own risk.
# Author: jsinix(jsinix.1337@gmail.com) 

use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Switch;

print header;
print start_html("Device Status DB");
my @fieldnames = param();
my $device = param('devicename');
chomp($device);
my $devicelen = length($device);

if($devicelen > 15) {
	print "Device name should be less than 15 characters.";
	exit();
}

my $description = param('description');
my $descriptionlen = length($description);
if($descriptionlen > 150) {
        print "Description should be less than 150 characters.";
        exit();
}

my $password = param('pass');
chomp($password);
#print $password;
#my $pwdbit0 = pass_bit($password);
#print $pwdbit0;
my $replacebit = param('replace');
chomp($replacebit);
my $selection = param('select');
chomp($selection);

switch ($selection) {
	case "add"	{add_entry($device, $description);}
	
	case "query"	{query_entry($device);}

	case "remove"	{remove_entry($device);}
	
	else {print "No valid option\n";}
}

sub add_entry {
	my ($dev1, $des1) = @_;
	my $pbit = is_present($dev1);
	my $pwdbit1 = pass_bit($password);
	if($pwdbit1 != 1) {
		print "Incorrect password";
		exit();
	}	
	if($pbit eq "1") {
		if($replacebit == 1) {
			create_device($dev1, $des1);
			print "Updated";
		} else {
			print "Device already present. If you want to replace select the 'Replace existing entry' and try again.";
		}
	} else {
		create_device($dev1, $des1);
		print "Created";
	}
}

sub query_entry {
        my ($dev2) = @_;
	my $qqbit = is_present($dev2);
	my $file_location = "DeviceDB/$dev2";
	if($qqbit == 1) {
		my $result1 = `cat $file_location`;
        	print $result1;
	} else {
		print "Entry not present";
	}
}

sub remove_entry {
	my ($dev5) = @_;
	my $ppbit = is_present($dev5);
	my $file_location = "DeviceDB/$dev5";
	my $pwdbit2 = pass_bit($password);	
	if($pwdbit2 != 1) {
                print "Incorrect password";
                exit();
        }
	if($ppbit == 1) {		
		`rm $file_location`;
		print "Entry removed";
	} else {
		print "Entry not present already";
	}
}

sub is_present {
	my ($dev3) = @_;
	my $file_location = "DeviceDB/";
	my $res = `ls -1 $file_location | grep $dev3`;
	if($res) {
		return 1;
	} else {
		return 0;
	}
}

sub create_device {
	my ($dev4,$des4) = @_;
	my $file_location = "DeviceDB/$dev4";
	open my $fh, '>', $file_location or die $!;
        print $fh $des4;
        close $fh;
}

sub pass_bit {
	my ($pass1) = @_;
	if($pass1 eq "12345") {
		return 1;
	} else {
		return 0;
	}
}

#my $link = "#";
#my $text = "Homepage";
#print "<br><br><br>";
#print "<a href=\"$link\">$text</a>"."\t";
print end_html;
