# AFD — Cajero Automático

## Caso práctico modelado

Este autómata finito determinista (AFD) representa el flujo de operación de un
**cajero automático**, desde que se inserta la tarjeta hasta que finaliza la
transacción y se expulsa la tarjeta.

**Alfabeto Σ = {a, b, c}**
- `a` → tecla numérica (ingresar un dígito del PIN, u opción "retirar efectivo" en el menú)
- `b` → confirmar / aceptar, u opción "consultar saldo" en el menú
- `c` → cancelar, o confirmar que el PIN ingresado es incorrecto

**Estados (7):**
| Estado | Significado |
|---|---|
| q0 | Inicio — tarjeta insertada |
| q1 | Ingresando PIN (dígito por dígito) |
| q2 | PIN incorrecto |
| q3 | Menú principal |
| q4 | Retirar efectivo |
| q5 | Consultar saldo |
| q6 | **Fin de operación / tarjeta expulsada (estado final)** |

**Estado inicial:** q0
**Estado(s) final(es):** F = {q6}

**Bucles (requisito de la rúbrica):**
- `q1` tiene un bucle con `a`: cada vez que se teclea un dígito del PIN se
  permanece en el mismo estado.
- `q4` tiene un bucle con `a`: se permanece en "Retirar efectivo" mientras se
  siguen pidiendo billetes o montos adicionales antes de confirmar.

## Función de transición δ

| Estado | a | b | c |
|---|---|---|---|
| → q0 | q1 | — | — |
| q1 | q1 (bucle) | q3 | q2 |
| q2 | q1 | — | q6 |
| q3 | q4 | q5 | q6 |
| q4 | q4 (bucle) | q6 | — |
| q5 | — | q6 | — |
| * q6 | — | — | — |

## Diagrama

El diagrama de estados se genera con el script `dfa_cajero_automatico.py`
(basado en el generador de AFD con `networkx` y `matplotlib` visto en clase).
Para verlo:

```bash
python dfa_cajero_automatico.py --diagrama
```

## Palabras de prueba

### 10 palabras aceptadas (terminan en q6)
| # | Palabra | Explicación |
|---|---|---|
| 1 | abab | PIN de 1 dígito correcto, retira efectivo sin monto extra |
| 2 | abbb | PIN correcto, consulta saldo |
| 3 | abc | PIN correcto, cancela en el menú |
| 4 | acc | PIN incorrecto, cancela de inmediato |
| 5 | aacc | PIN de 2 dígitos incorrecto, cancela |
| 6 | aaabab | PIN de 3 dígitos correcto, retira efectivo |
| 7 | acabc | PIN incorrecto, reintenta, esta vez correcto, cancela en el menú |
| 8 | aaabc | PIN de 3 dígitos correcto, cancela en el menú |
| 9 | aabaab | PIN de 2 dígitos correcto, retira efectivo pidiendo 2 montos |
| 10 | acaabc | PIN incorrecto, reintenta con 2 dígitos, correcto, cancela |

### 5 palabras rechazadas
| # | Palabra | Motivo |
|---|---|---|
| 1 | a | Se queda ingresando el PIN (q1), nunca confirma |
| 2 | ab | Llega al menú (q3) pero no elige ninguna opción |
| 3 | ac | PIN incorrecto (q2), nunca cancela ni reintenta |
| 4 | aba | Entra a "retirar efectivo" (q4) pero no confirma |
| 5 | cab | Símbolo `c` inválido desde el estado inicial q0 (no existe transición) |

## Ejecución

```bash
pip install matplotlib networkx

# Simular y animar una cadena puntual
python dfa_cajero_automatico.py abab

# Correr automáticamente las 15 palabras de prueba (reporta ACEPTA/RECHAZA)
python dfa_cajero_automatico.py --test

# Ver solo el diagrama de estados
python dfa_cajero_automatico.py --diagrama
```

## Integrantes del equipo
- Nombre 1
- Nombre 2
- Nombre 3
