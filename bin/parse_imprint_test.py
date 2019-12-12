#!/usr/bin/env python3

import unittest
from parse_imprint import preprocess, basic_match

test_list = ["Printed [by B. Alsop and T. Fawcet] for H. Holland and G. Gibbs, at the Golden Flower-deluce in Popes-head Alley", "Printed for Michael Sparke Senior, at the Blew Bible in Greene Arbor", "Printed by Reinier Leers, and are to be sold by Nicholas Cox near Queens Colledge Oxon.", "Printed by J[ames]. Rawlins, for John Place at Furnivals-Inn-gate in Holborn", "Imprinted [by the successors of G. Thorp]","Printed by Andrew Crook and Samuel Helsham, assigns of Benjamin Tooke, printer to the Kings most excellent Majesty, and are to be sold by Andrew Crook, at his Majesties printing-house on Ormonde-Key, and by Samuel Helsham, at the Colledge-Arms in Castle-street.", "printed for Randall Taylor, near Stationers-Hall", "Printed at Holy-Rood House, by James Watson, printer to His Most Sacred Majesties royal family and houshould, reprinted by G. Croom, at the Blue Ball in Thames-street, near Baynards Castle","Printed for William Hope, at the blew Anchor, behind the Old Exchange, and Henry Herringman, at the blew Anchor in the lower walk in the New Exchange.","Printed for R. Sare ... F. Saunders ... and Tho. Bennet ...", "Printed by Edward Jones in the Savoy, and sold by Jacob Tonson in Fleet-Street, and John Nutt near Stationers-Hall"]

preprocessed = ['Printed [by B. Alsop and T. Fawcet] for H. Holland and for G. Gibbs, at the Golden Flower-deluce in Popes-head Alley', 'Printed for Michael Sparke Senior, at the Blew Bible in Greene Arbor', 'Printed by Reinier Leers, and are to be sold by Nicholas Cox near Queens Colledge Oxon.', 'Printed by J[ames]. Rawlins, for John Place at Furnivals-Inn-gate in Holborn', 'Imprinted [by the successors of G. Thorp]', 'Printed by Andrew Crook and Samuel Helsham, assigns of Benjamin Tooke, printer to the Kings most excellent Majesty, and are to be sold by Andrew Crook, at his Majesties printing-house on Ormonde-Key, and sold by Samuel Helsham, at the Colledge-Arms in Castle-street.', 'printed for Randall Taylor, near Stationers-Hall', 'Printed at Holy-Rood House, by James Watson, printer to His Most Sacred Majesties royal family and houshould, reprinted by G. Croom, at the Blue Ball in Thames-street, near Baynards Castle', 'Printed for William Hope, at the blew Anchor, behind the Old Exchange, and for Henry Herringman, at the blew Anchor in the lower walk in the New Exchange.', 'Printed for R. Sare ... F. Saunders ... and for Tho. Bennet ...', 'Printed by Edward Jones in the Savoy, and sold by Jacob Tonson in Fleet-Street, and sold by John Nutt near Stationers-Hall']

matched = [{'publisher': ['G. Gibbs', 'H. Holland'], 'location': ['the Golden Flower-deluce in Popes-head Alley'], 'bookseller': [], 'patron': [], 'printer': ['B. Alsop', 'T. Fawcet]'], 'assigns': []}, {'publisher': ['Michael Sparke Senior'], 'location': ['the Blew Bible in Greene Arbor'], 'bookseller': [], 'patron': [], 'printer': [], 'assigns': []}, {'publisher': [], 'location': ['Queens Colledge Oxon.'], 'bookseller': ['Nicholas Cox'], 'patron': [], 'printer': ['Reinier Leers'], 'assigns': []}, {'publisher': ['John Place'], 'location': ['Furnivals-Inn-gate in Holborn'], 'bookseller': [], 'patron': [], 'printer': ['J[ames]. Rawlins'], 'assigns': []}, {'publisher': [], 'location': [], 'bookseller': [], 'patron': [], 'printer': ['the successors of G. Thorp]'], 'assigns': []}, {'publisher': [], 'location': ['his Majesties printing-house on Ormonde-Key', 'the Colledge-Arms in Castle-street.'], 'bookseller': ['Andrew Crook', 'Samuel Helsham'], 'patron': ['the Kings most excellent Majesty'], 'printer': ['Andrew Crook', 'Samuel Helsham'], 'assigns': ['Benjamin Tooke']}, {'publisher': ['Randall Taylor'], 'location': ['Stationers-Hall'], 'bookseller': [], 'patron': [], 'printer': [], 'assigns': []}, {'publisher': [], 'location': ['Holy-Rood House', 'the Blue Ball in Thames-street, near Baynards Castle'], 'bookseller': [], 'patron': ['His Most Sacred Majesties royal family and houshould'], 'printer': ['G. Croom', 'James Watson'], 'assigns': []}, {'publisher': ['Henry Herringman', 'William Hope'], 'location': ['the blew Anchor in the lower walk in the New Exchange.', 'the blew Anchor, behind the Old Exchange'], 'bookseller': [], 'patron': [], 'printer': [], 'assigns': []}, {'publisher': ['F. Saunders', 'R. Sare', 'Tho. Bennet'], 'location': [], 'bookseller': [], 'patron': [], 'printer': [], 'assigns': []}, {'publisher': [], 'location': ['Fleet-Street', 'Stationers-Hall', 'the Savoy'], 'bookseller': ['Jacob Tonson', 'John Nutt'], 'patron': [], 'printer': ['Edward Jones'], 'assigns': []}]

class TestParse(unittest.TestCase):

	def test_preprocess(self):
		for i,t in enumerate(test_list):
			self.assertEqual(preprocess(t), preprocessed[i])

	def test_basic_match(self):
		for i,t in enumerate(preprocessed):
			self.assertEqual(basic_match(t), matched[i])

if __name__=="__main__":
	unittest.main()
	#prep = [preprocess(t) for t in test_list]
	#print(prep)
	#match = [basic_match(p) for p in preprocessed]
	#print(match)
