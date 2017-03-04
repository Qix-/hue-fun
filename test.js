var ELEMENTS = [
        "Ac", "Ag", "Al", "Am", "Ar", "As", "At", "Au",
	    "B", "Ba", "Be", "Bh", "Bi", "Bk", "Br", "C",
	    "Ca", "Cd", "Ce", "Cf", "Cl", "Cm", "Cn", "Co",
	    "Cr", "Cs", "Cu", "Db", "Ds", "Dy", "Er", "Es",
	    "Eu", "F", "Fe", "Fl", "Fm", "Fr", "Ga", "Gd",
	    "Ge", "H", "He", "Hf", "Hg", "Ho", "Hs", "I",
	    "In", "Ir", "K", "Kr", "La", "Li", "Lr", "Lu",
	    "Lv", "Md", "Mg", "Mn", "Mo", "Mt", "N", "Na",
	    "Nb", "Nd", "Ne", "Ni", "No", "Np", "O", "Os",
	    "P", "Pa", "Pb", "Pd", "Pm", "Po", "Pr", "Pt",
	    "Pu", "Ra", "Rb", "Re", "Rf", "Rg", "Rh", "Rn",
	    "Ru", "S", "Sb", "Sc", "Se", "Sg", "Si", "Sm",
	    "Sn", "Sr", "Ta", "Tb", "Tc", "Te", "Th", "Ti",
	    "Tl", "Tm", "U", "Uuo", "Uup", "Uus", "Uut", "V",
	    "W", "Xe", "Y", "Yb", "Zn", "Zr"
    ];

var r = new RegExp('(' + ELEMENTS.sort().reverse().join('|') + ')', 'ig');

function camelBracket(m) {
    m = m.toLowerCase();
    return '[' + m[0].toUpperCase() + m.substring(1) + ']';
}

function convert(name) {
    return name.replace(r, camelBracket);
}

console.log(convert(process.argv[2]));