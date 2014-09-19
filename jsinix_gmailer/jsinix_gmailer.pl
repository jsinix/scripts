#!/usr/bin/perl
use strict;
use warnings;
use Mail::POP3Client;
use IO::Socket::SSL;
use CGI qw(:standard);
use Net::SMTP::TLS;
# There will be a bug using the Net::SMTP::TLS module
# So the fix i found here:
# http://crunchbang.org/forums/viewtopic.php?pid=361299
# invalid SSL_version specified at /usr/share/perl5/IO/Socket/SSL.pm line
# replace this: m{^(!?)(?:(SSL(?:v2|v3|v23|v2/3))|(TLSv1[12]?))$}i
# with this: m{^(!?)(?:(SSL(?:v2|v3|v23|v2/3))|(TLSv1[12]?))}i
use Term::ReadKey;
use Switch;
use Mail::IMAPClient;
use Term::ANSIColor qw(:constants);
use Crypt::DES;
use Crypt::Lite;

# Declaring all variables
my $cgi;
my $username;
my $password;
my $mailhost;
my $port;
my $pop;
my $count;
my $i;
my $uname;
my $pass;
my $emailto;
my $emailbody;
my $mailer;
my $emaillogin;
my $uname1;
my $pass1;
my $choice = '';
my $emailbodyfin;
my $emailbodyplain;
my $enckey1;
my $cipher;
my $ciphertext1;
my $encrypted;
my $crypt;
my $emailbodyplain1;
my $enckey2;
my $decryptedmsg = '';
my $dcrypt;
my $decrypted;
my $encryptedmsg = '';
my $enckey3;
my $emailbodyplain2;

while ($choice ne '5') {
	START:
	system("clear");
	
	print BOLD, BLUE, "\n\n\n\n\tJSINIX Gmailer\n\n", RESET;
	print "\n\t1. Send email".
	      "\n\t2. Check email".
	      "\n\t3. Encrypt email".	
	      "\n\t4. Decrypt email".	
	      "\n\t5. Quit(q)";	
	
	print "\n\n\tChoice: ";
	$choice = <STDIN>;
	chomp($choice);
	
	switch ($choice) {

		case '1'
		{
			system("clear");
			mail_send();
			print "\n\tPress enter to continue"; <STDIN>; 
			goto START;
		}

		case '2'
		{
			system("clear");
			mail_check_pop();
			print "\n\tPress enter to continue"; <STDIN>; 
                        goto START;
		}

		case '3'
		{
                        system("clear");
                        mail_encrypt();
                        print "\n\tPress enter to continue"; <STDIN>;
                        goto START;
			
		}

		case '4'
		{
                        system("clear");
                        mail_decrypt();
			#encdec('test','test');
                        print "\n\tPress enter to continue"; <STDIN>;
                        goto START;
		
		}

		case '5'
		{
			system("clear");
                        exit();
		}

		case 'q'
                {
                        system("clear");
                        exit();
                }		

	}
}

sub mail_check_pop { 
	$cgi = new CGI;

	($uname1, $pass1) = get_credentials();

	$mailhost = 'pop.gmail.com';
	$port = '995';

	$pop = Mail::POP3Client->new(USER=> $uname1,
		PASSWORD => $pass1,
		HOST => $mailhost,
		PORT => $port,
		USESSL => 'true',
		DEBUG => 0,) or die("\n\tERROR: Unable to connect to mail server.\n");

	$count = $pop->Count();

	if (($pop->Count()) < 1)
	{
		print "\n\tNo messages...\n";
		print "\n\tPress enter to continue"; <STDIN>;
		goto START;
	}

	print "\n\tThere are $count Messages in your inbox\n";
	
	print "How many messages you want to print: ";
	my $eno = <STDIN>;
	chomp($eno);	

	for(my $i = 1; $i <= $eno; $i++)
		{
			print "\n\n\nMail number $1\n";
			foreach($pop->Head($i))
			{
				/^(From|Subject|Email):\s+/i && print $_, "\n";
			}
		print 'Message: '.$pop->Body($i);
		}	

	$pop->Close();

}

mail_send();
sub mail_send {

	print "\n\tLogin ID: ";
	my $uname2 = get_user();
	print "\n\tPassword: ";
	my $pass2 = get_pass();

	print "\n\tMail To: ";
	my $emailto = <STDIN>;
	chomp($emailto);

	print "\n\tBody: ";
	$emailbodyplain = get_body(); 

	print "\n\tWant to encrypt body ?(y/n)";
	my $echoice = <STDIN>;
	chomp($echoice);

	if ($echoice eq 'y') {
		
		print "\n\tEncryption key: ";
		$enckey1 = get_pass();	
		$emailbodyfin = encrypt_body($emailbodyplain, $enckey1);
		
	}
	elsif ($echoice eq 'n') {
		$emailbodyfin = $emailbodyplain;
	} 
	else {
		print "\n\tWrong selection my friend";
	}

	my $mailer = new Net::SMTP::TLS(
		'smtp.gmail.com',
		Hello => 'smtp.gmail.com',
		Port => 587,
		User => $uname2,
		Password=> $pass2);

		$mailer->mail($emailto);
		$mailer->to($emailto);
		$mailer->data;
		$mailer->datasend($emailbodyfin);
		$mailer->dataend;
		$mailer->quit;
		print "\n\tEmail sent.";
}

sub mail_encrypt {

        print "\n\n\tEncrypt message\n\n";

        print "\n\tPlain text/body: ";
        $emailbodyplain2 = get_body();

        print "\n\tEncryption key: ";
        $enckey3 = get_pass();

        my $encryptedmsg1 = encrypt_body($emailbodyplain2, $enckey3);

        print "\n\tEncrypted message: "; print $encryptedmsg1;

}

sub mail_decrypt {
	
	print "\n\n\tDecrypt message\n\n";

	print "\n\tEncrypted text/body: ";
	$emailbodyplain1 = get_body();
	
	print "\n\tDecryption key: ";
	$enckey2 = get_pass();

	my $decryptedmsg1 = decrypt_body($emailbodyplain1, $enckey2);
	
	print "\n\tDecrypted message: "; print $decryptedmsg1;
}

sub get_user {
   
	my $emaillogin = <STDIN>;
        chomp($emaillogin);
		
	return $emaillogin;
}

sub get_pass {

	ReadMode('noecho');
	chomp(my $password = <STDIN>);
	ReadMode(0);

	return $password;
}

sub mail_check_imap {

	my ($uname3, $pass3) = get_credentials();

	my $imap = Mail::IMAPClient->new ( Server => 'imap.gmail.com',
                                User => $uname3,
                                Password => $pass3,
                                Port => 993,
                                Ssl => 1,
                                Uid => 1 )
	or die "\n\tCould not connect to server, terminating...\n";
}

sub get_body {
 
        my $emailbody = <STDIN>;
        chomp($emailbody);

	return $emailbody;
}

$crypt = Crypt::Lite->new( debug => 0, encoding => 'hex8' );

sub encrypt_body {
	
	my ($pbody1, $epass1) = $_;
	$crypt = Crypt::Lite->new( debug => 0, encoding => 'hex8' );
	$encrypted = $crypt->encrypt($pbody1, $epass1);
	
	return $encrypted;
}

sub decrypt_body {

        my ($pbody2, $epass2) = $_;
        $crypt = Crypt::Lite->new( debug => 0, encoding => 'hex8' );
        $decrypted = $crypt->decrypt($pbody2, $epass2);

        return $decrypted;
}
