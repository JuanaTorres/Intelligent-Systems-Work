mensaje=""
def preferencia():
  mensaje="Sus notas no son la ideales"
  print("Sus notas no son la ideales")
  
def preferencia1():
  listPreferencias={}
  for a,v in params.items():
    if a== "ingenieria" or a== "humanidades" or a== "ciencias" or  a== "salud":
      listPreferencias[a]=v
  carrera=max(listPreferencias, key=listPreferencias.get)
  mensaje=f"Por su preferencia va a estudiar{carrera}"
  print("Por su preferencia va a estudiar")
  print(carrera)

def preferencia2():
  print("Puede estudiar Ingenieria o Ciencias")
  listPreferencias={}
  for a,v in params.items():
    if a== "ingenieria" or a== "ciencias":
      listPreferencias[a]=v
  carrera=max(listPreferencias, key=listPreferencias.get)
  mensaje=f"Puede estudiar Ingenieria o Ciencias \n Por su preferencia va a estudiar{carrera}"
  print("Por su preferencia va a estudiar")
  print(carrera)

def preferencia3():
  print("Puede estudiar Humanidades o Salud")
  listPreferencias={}
  for a,v in params.items():
    if a== "humanidades" or  a== "salud":
      listPreferencias[a]=v
  carrera=max(listPreferencias, key=listPreferencias.get)
  mensaje=f"Puede estudiar Humanidades o Salud \n Por su preferencia va a estudiar{carrera}"
  print("Por su preferencia va a estudiar")
  print(carrera)

def preferencia4():
  mensaje="Puede estudiar Humanidades."
  print("Puede estudiar Humanidades.")

def preferencia5():
  mensaje="Puede estudiar Humanidades."
  print("Puede estudiar Humanidades.")

def preferencia6():
  mensaje="Puede estudiar Ingenieria."
  print("Puede estudiar Ingenieria.")

def preferencia7():
  
  print("Puede estudiar Ciencias o Humanidades.")
  listPreferencias={}
  for a,v in params.items():
    if  a== "humanidades" or a== "ciencias" :
      listPreferencias[a]=v
  carrera=max(listPreferencias, key=listPreferencias.get)
  mensaje=f"Puede estudiar Ciencias o Humanidades \n Por su preferencia va a estudiar{carrera}"
  print("Por su preferencia va a estudiar")
  print(carrera)

def preferencia8():
  mensaje="Puede estudiar Ciencias."
  print("Puede estudiar Ciencias.")

params = {}
print("Por favor ingrese los valores para las siguientes categorías:")
categorias = ['matematicas', 'escritura', 'cienciasNat', 'cienciasSoc', 'ingles', 'ingenieria', 'humanidades', 'ciencias', 'salud']
for categoria in categorias:
    valor = input(f"Ingrese el valor para {categoria}: ")
    params[categoria] = int(valor)

rules=""
with open("./reglas.txt", "r") as file:
    rules += file.read()

import sys
from business_rule_engine import RuleParser
from business_rule_engine.exceptions import MissingArgumentError
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
parser = RuleParser()
parser.register_function(preferencia)
parser.register_function(preferencia1)
parser.register_function(preferencia2)
parser.register_function(preferencia3)
parser.register_function(preferencia4)
parser.register_function(preferencia5)
parser.register_function(preferencia6)
parser.register_function(preferencia7)
parser.register_function(preferencia8)

parser.parsestr(rules)
for rule in parser:
    try:
        rvalue_condition, rvalue_action = rule.execute(params)
        if rule.status:
            print(rvalue_action)
            break
    except MissingArgumentError:
        pass
print(mensaje)