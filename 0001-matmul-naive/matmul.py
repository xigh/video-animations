from manimlib import *

class MatrixMultiplication(Scene):
    def construct(self):
        title = Text("Multiplication de matrices", font_size=48)
        title.shift(UP * 3)
        subtitle = Text("de dimensions 3x2 et 2x4", font_size=36)
        subtitle.next_to(title, DOWN)
        self.add(title, subtitle)

        # Données réelles
        data_A = [[1, 2],
                  [3, 4],
                  [5, 6]]

        data_B = [[1, 2, 3, 4],
                  [5, 6, 7, 8]]

        # Matrices visuelles
        A = Matrix(data_A)
        B = Matrix(data_B)

        # Positionnement
        A.shift(LEFT * 4)
        B.shift(LEFT * 0.8)

        # Affichage initial
        self.play(Write(A, stroke_color=YELLOW), Write(B, stroke_color=BLUE))
        self.wait(0.5)

        # Symboles × et =
        times = Tex(r"\times").next_to(A, RIGHT)
        equals = Tex("=").next_to(B, RIGHT)

        self.play(Write(times))
        self.play(Write(equals))
        self.wait(0.5)

        A_lines = len(A.get_rows())
        A_cols = len(A.get_columns())
        B_cols = len(B.get_columns())
        # B_lines = len(B.get_rows())

        # Matrice résultat avec placeholders
        C = Matrix([[ "?" for _ in range(B_cols)] for _ in range(A_lines)])
        C.next_to(equals, RIGHT)
        self.play(Write(C, stroke_color=RED))
        self.wait(0.5)

        # Zone pour affichage du calcul
        calc_area = Tex("").shift(DOWN * 2)

        # Compteurs d'opérations
        additions = 0
        multiplications = 0
        loads = 0
        stores = 0

        # Créer l'affichage des compteurs en bas
        counter_text = Tex(
            f"Additions: {additions} \\quad "
            f"Multiplications: {multiplications} \\quad "
            f"Loads: {loads} \\quad "
            f"Stores: {stores}"
        ).shift(DOWN * 3.5)
        self.add(counter_text)

        # Facteur d'accélération initial
        speed_factor = 1.0

        def update_counter_text():
            new_counter_text = Tex(
                f"Additions: {additions} \\quad "
                f"Multiplications: {multiplications} \\quad "
                f"Loads: {loads} \\quad "
                f"Stores: {stores}"
            ).shift(DOWN * 3.5)
            self.play(Transform(counter_text, new_counter_text), run_time=0.2/speed_factor)

        for i in range(A_lines):      # lignes de A
            for j in range(B_cols):  # colonnes de B
                # Surligner ligne et colonne
                row_highlight = SurroundingRectangle(VGroup(*A.get_rows()[i]), color=YELLOW, buff=0.2)
                col_highlight = SurroundingRectangle(VGroup(*B.get_columns()[j]), color=BLUE, buff=0.2)
                self.play(ShowCreation(row_highlight), ShowCreation(col_highlight), run_time=0.8/speed_factor)

                # Construire la formule terme par terme
                # formula_terms = []
                current_formula = ""
                
                for k in range(A_cols):
                    # Load des valeurs depuis les matrices
                    loads += 4
                    update_counter_text()
                    
                    # Créer les copies des nombres pour ce terme
                    num_A = Tex(str(data_A[i][k])).move_to(A.get_entries()[i*A_cols + k].get_center())
                    num_A.set_color(YELLOW)
                    
                    num_B = Tex(str(data_B[k][j])).move_to(B.get_entries()[k*B_cols + j].get_center())
                    num_B.set_color(BLUE)
                    
                    self.add(num_A, num_B)
                    
                    # Positions cibles dans la zone de calcul (même niveau horizontal)
                    if k == 0:
                        calc_pos_A = calc_area.get_center() + LEFT * 1.5
                        calc_pos_B = calc_area.get_center() + RIGHT * 1.5
                    else:
                        calc_pos_A = calc_area.get_center() + LEFT * 1.5
                        calc_pos_B = calc_area.get_center() + RIGHT * 1.5
                    
                    # Créer les versions cibles
                    target_A = Tex(str(data_A[i][k])).move_to(calc_pos_A)
                    target_A.set_color(YELLOW)
                    target_B = Tex(str(data_B[k][j])).move_to(calc_pos_B)
                    target_B.set_color(BLUE)
                    
                    # Animer le déplacement des nombres
                    self.play(
                        Transform(num_A, target_A),
                        Transform(num_B, target_B),
                        run_time=0.8/speed_factor
                    )
                    self.wait(0.3/speed_factor)
                    
                    # Multiplication quand les nombres arrivent dans la zone de calcul
                    multiplications += 1
                    update_counter_text()
                    
                    # Construire le terme
                    if k == 0:
                        term = f"{data_A[i][k]}\\times{data_B[k][j]}"
                    else:
                        term = f" + {data_A[i][k]}\\times{data_B[k][j]}"
                        # Addition quand le deuxième terme arrive
                        additions += 1
                        update_counter_text()
                    
                    current_formula += term
                    formula_tex = Tex(current_formula).move_to(calc_area)
                    
                    # Afficher le terme avec fade
                    self.play(
                        Transform(calc_area, formula_tex),
                        FadeOut(num_A),
                        FadeOut(num_B),
                        run_time=0.5/speed_factor
                    )
                    self.wait(0.3/speed_factor)
                
                # Calculer et afficher le résultat
                value = sum(data_A[i][k] * data_B[k][j] for k in range(2))
                final_formula = f"{current_formula} = {value}"
                final_tex = Tex(final_formula).move_to(calc_area)
                
                self.play(Transform(calc_area, final_tex), run_time=0.8/speed_factor)
                self.wait(0.8/speed_factor)

                # Créer le résultat qui va se déplacer
                result_num = Tex(str(value)).move_to(calc_area.get_center())
                result_num.set_color(RED)
                self.add(result_num)

                # Créer la version cible du résultat pour l'animation
                target_result = Tex(str(value)).move_to(C.get_entries()[i*B_cols + j].get_center())
                target_result.set_color(RED)
                
                # Animer le résultat vers la matrice C
                self.play(Transform(result_num, target_result), run_time=1.0/speed_factor)
                
                # Store du résultat dans la matrice C
                stores += 1
                update_counter_text()
                
                # Remplacer le placeholder par le résultat
                self.play(Transform(C.get_entries()[i*B_cols + j], result_num), run_time=0.5/speed_factor)
                
                # Nettoyer le résultat temporaire
                self.remove(result_num)

                # Retirer surlignages
                self.remove(row_highlight, col_highlight)
                
                # Faire disparaître le calcul intermédiaire avant la prochaine étape
                if i < A_lines - 1 or j < B_cols - 1:  # Pas à la dernière itération
                    self.play(FadeOut(calc_area), run_time=0.3/speed_factor)
                    # Recréer la zone vide pour la prochaine étape
                    calc_area = Tex("").shift(DOWN * 2)
                
                self.wait(0.2/speed_factor)

                # Augmenter la vitesse pour la prochaine itération (accélération de 20%)
                speed_factor *= 1.5

        self.wait(2)
