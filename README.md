Following the paper from Zaragoza et. al., 'Web Search Solved?', and adapted for the Cross Lingual Lexical Substitution task at SemEval 2010, takes a CSV file of the format

"serial number","system","query/ item","score"
"1","ColEur","about.r",0.5
...
...

etc, uses Python and matplotlib to generate plots for each pair of systems in the data.

The CSV file must be in the current directory (change the path in the code). It should contain data in the above format, and the data would be a list of systems, the item/ query they are trying to solve and the score obtained. Can be modified to fit a variety of tasks. Two sample graphs are attached too. As the graphs depict, it is a nice way to visualize how the systems compare against each other.

You will need matplotlib installed for this to work. Just do 'python disruptiveSetAnalyzer.py' from the shell.

To install matplotlib, just do a sudo apt-get install matplotlib on Ubuntu; check the Web for your Linux flavor.

You can change the DELTA values in the code to reflect your own personal
needs; initially it is set to reflect a range of 0 to 10. Please refer to the
paper listed at the top for further information, or just contact me. The
code, if executed properly, will produce one graph for each pair of
systems.

~Ambidextrous (Ravi)
Mar, 2011
Updated: Jan 2013

PS: Please report all bugs to ravisinha AT my DOT unt DOT edu. The application worked fantastic when I wrote it, but certain modifications might be needed for your specific requirements.
