#! /usr/bin/env python3

import unittest
from parse_imprint import preprocess, basic_match

test_list = ["Printed [by B. Alsop and T. Fawcet] for H. Holland and G. Gibbs, at the Golden Flower-deluce in Popes-head Alley", "Printed for Michael Sparke Senior, at the Blew Bible in Greene Arbor", "Printed by Reinier Leers, and are to be sold by Nicholas Cox near Queens Colledge Oxon.", "Printed by J[ames]. Rawlins, for John Place at Furnivals-Inn-gate in Holborn", "Imprinted [by the successors of G. Thorp]","Printed by Andrew Crook and Samuel Helsham, assigns of Benjamin Tooke, printer to the Kings most excellent Majesty, and are to be sold by Andrew Crook, at his Majesties printing-house on Ormonde-Key, and by Samuel Helsham, at the Colledge-Arms in Castle-street.", "printed for Randall Taylor, near Stationers-Hall", "Printed at Holy-Rood House, by James Watson, printer to His Most Sacred Majesties royal family and houshould, reprinted by G. Croom, at the Blue Ball in Thames-street, near Baynards Castle"]

preprocessed = ['Printed [by B. Alsop and T. Fawcet] for H. Holland and G. Gibbs, at the Golden Flower-deluce in Popes-head Alley', 'Printed for Michael Sparke Senior, at the Blew Bible in Greene Arbor', 'Printed by Reinier Leers, and are to be sold by Nicholas Cox near Queens Colledge Oxon.', 'Printed by J[ames]. Rawlins, for John Place at Furnivals-Inn-gate in Holborn', 'Imprinted [by the successors of G. Thorp]', 'Printed by Andrew Crook and Samuel Helsham, assigns of Benjamin Tooke, printer to the Kings most excellent Majesty, and are to be sold by Andrew Crook, at his Majesties printing-house on Ormonde-Key, and by Samuel Helsham, at the Colledge-Arms in Castle-street.', 'printed for Randall Taylor, near Stationers-Hall', 'Printed at Holy-Rood House, by James Watson, printer to His Most Sacred Majesties royal family and houshould, reprinted by G. Croom, at the Blue Ball in Thames-street, near Baynards Castle']

matched = [{'patron': [], 'printer': ['B. Alsop', 'T. Fawcet]'], 'publisher': ['G. Gibbs', 'H. Holland'], 'bookseller': [], 'location': ['the Golden Flower-deluce in Popes-head Alley'], 'assigns': []}, {'patron': [], 'printer': [], 'publisher': ['Michael Sparke Senior'], 'bookseller': [], 'location': ['the Blew Bible in Greene Arbor'], 'assigns': []}, {'patron': [], 'printer': ['Reinier Leers'], 'publisher': [], 'bookseller': ['Nicholas Cox'], 'location': ['Queens Colledge Oxon.'], 'assigns': []}, {'patron': [], 'printer': ['J[ames]. Rawlins'], 'publisher': ['John Place'], 'bookseller': [], 'location': ['Furnivals-Inn-gate in Holborn'], 'assigns': []}, {'patron': [], 'printer': ['the successors of G. Thorp]'], 'publisher': [], 'bookseller': [], 'location': [], 'assigns': []}, {'patron': ['the Kings most excellent Majesty'], 'printer': ['Andrew Crook', 'Samuel Helsham'], 'publisher': [], 'bookseller': ['Andrew Crook'], 'location': ['his Majesties printing-house on Ormonde-Key', 'the Colledge-Arms in Castle-street.'], 'assigns': ['Benjamin Tooke']}, {'patron': [], 'printer': [], 'publisher': ['Randall Taylor'], 'bookseller': [], 'location': ['Stationers-Hall'], 'assigns': []}, {'patron': ['His Most Sacred Majesties royal family and houshould'], 'printer': ['G. Croom', 'James Watson'], 'publisher': [], 'bookseller': [], 'location': ['Holy-Rood House', 'the Blue Ball in Thames-street, near Baynards Castle'], 'assigns': []}]


class TestParse(unittest.TestCase):

	def test_preprocess(self):
		for i,t in enumerate(test_list):
			self.assertEqual(preprocess(t), preprocessed[i])

	def test_basic_match(self):
		for i,t in enumerate(test_list):
			self.assertEqual(basic_match(t), matched[i])

if __name__=="__main__":
	unittest.main()
	#match = [basic_match(t) for t in test_list]
	#print(match)
