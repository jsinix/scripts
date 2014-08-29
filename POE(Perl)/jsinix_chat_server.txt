#!/usr/bin/perl
#Author JSINIX
#This is a small multiple client chat server.
#Please feel free to use.
use warnings;
use strict;
use POE;
use POE::Component::Server::TCP;

POE::Component::Server::TCP->new(
	Alias              => "matanay_comm",
	Port               => 1337,
  	InlineStates       => {send => \&handle_send},
  	ClientConnected    => \&client_connected,
  	ClientError        => \&client_error,
  	ClientDisconnected => \&client_disconnected,
  	ClientInput        => \&client_input,
);
$poe_kernel->run();
exit 0;

my %users;

sub broadcast {
	my ($sender, $msg, $ip) = @_;
	foreach my $user (keys %users) {
		if ($user eq $sender) {
		$poe_kernel->post($user => send => "Me >> $msg");
		}
    		else {
      		$poe_kernel->post($user => send => "$ip >>  $msg");
    		}	
  	}
}

sub handle_send {
	my ($heap, $msg) = @_[HEAP, ARG0];
	$heap->{client}->put($msg);
}

sub client_connected {
	my $session_id = $_[SESSION]->ID;
	$users{$session_id} = 1;
	broadcast($session_id," *** connected ***","$_[HEAP]{remote_ip}");
	print "";
}

sub client_disconnected {
	my $session_id = $_[SESSION]->ID;
	delete $users{$session_id};
	broadcast($session_id," *** disconnected ***","$_[HEAP]{remote_ip}");
}

sub client_error {
	my $session_id = $_[SESSION]->ID;
	delete $users{$session_id};
	broadcast($session_id," *** disconnected ***","$_[HEAP]{remote_ip}");
	$_[KERNEL]->yield("shutdown");
}

sub client_input {
	my ($kernel, $session, $input) = @_[KERNEL, SESSION, ARG0];
	my $session_id = $session->ID;
	my $len = length($input);
	if ( $len > 50 ) {
	broadcast($session_id,"Short messages please!","$_[HEAP]{remote_ip}");
	}
	else {
	broadcast($session_id,"$input","$_[HEAP]{remote_ip}");
	}

	my $exitcode = "byejassbye";
	
	if ($input eq $exitcode) {
		exit 0;
	}
}
