import re



def test_match(s,essay):
	count = 0
	if re.match(essay, s):
		count = count + 1
    return count

def findEmoticonCount(essay)
{
	should_match = [
    ':)',   # Single smile
    ':(',   # Single frown
    ':):)', # Two smiles
    ':(:(', # Two frowns
    ':):(', # Mix of a smile and a frown
    '(*_*)',
    ':">',
    ';)',
	':D',
	':->',
	':P',
	'<3',
	'</3',
	':O',
	'XD',
	'>:(',
	'D:<',
	'=K',
	':s',
	';P',
	'=)',
	'=O)',
	':-)',
	':^)',
	'=)',
	':O',
	';-)'
	]

	count = 0
	for x in should_match: 
		count = count + test_match(x);

	return count

}

