<?php
$nome = "João";
$idade = 25;
$altura = 1.75;

if ($idade >= 18) {
    echo "{$nome} é maior de idade\n";
} else {
    echo "{$nome} é menor de idade\n";
}

for ($i = 0; $i < 10; $i++) {
    print "Contagem: $i\n";
}

function soma($a, $b) {
    return $a + $b;
}
?>