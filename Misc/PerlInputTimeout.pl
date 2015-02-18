# Permission to use, copy, modify and distribute this 
# software and its documentation for any purpose and 
# without fee is hereby granted, provided that the above 
# copyright notice appear in all copies that both 
# copyright notice and this permission notice appear in 
# supporting documentation. jsinix makes no representations 
# about the suitability of this software for any purpose. 
# It is provided "as is" without express or implied warranty.

# jsinix DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, 
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. 
# IN NO EVENT SHALL jsinix BE LIABLE FOR ANY SPECIAL, INDIRECT 
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM 
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, 
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN 
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

#!/usr/bin/perl
# This is a script that demonstrates 
# how to get input from keyboard 
# with a timeout. This can be useful
# in many places.

use strict;
use warnings;

sub ask_data {
    my ($tout) = @_;	
    my $answer;

    print "Enter the data before $tout seconds: ";
    eval {
        local $SIG{ALRM} = sub { die "timeout reading from keyboard" };
        alarm $tout;
        $answer = <STDIN>;
        alarm 0;
        chomp $answer;
    };
    if ($@) {
        die $@ if $@ ne "timeout reading from keyboard";
        $answer = 'No answer given';
    }
    return $answer;
}

my $data = ask_data('10');
print "nThe answer is: " . $data . "n";

