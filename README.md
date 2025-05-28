Geometry Arsch

Teilnehmer: Leon Geller, Carlos Kohl

2AHET

26.05.2025


In unserem Projekt Geometry Arsch geht es um eine billige Kopie des Spiels Geometry Dash.

Das Ziel ist ein simples Level zu erstellen, welches man selbst ändern kann.

Es soll nicht zu kompliziert und einfach zu bedienen sein.


Aufteilung:

Wir haben das Projekt nicht in 2 Teile aufgeteil sondern Code with me verwendet um gemeinsam zu coden.

So konnten wir beide unserer Ideen umsetzen und es war allgemein angenehmer und hat mehr Spaß gemacht als allein zu coden.


Teil des Codes:

If     game_state == MENU:
        title_font = pygame.font.SysFont(None, 72)
        title_text = title_font.render('GEOMETRY ASS', True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

        level_text = font.render(f"Level: {level_name}", True, BLACK)
        screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 - 50))

        instruction_text = font.render("Press SPACE to Start", True, BLACK)
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2))

Dieser Code zeigt im Spielzustand MENU drei Texte auf dem Bildschirm an:

1. Titel: "GEOMETRY ASS" – groß und zentriert im oberen Drittel.

2. Level-Anzeige: Aktuelles Level (den Level Namen)– zentriert in der Bildschirmmitte.

3. Anweisung: "Press SPACE to Start" – gibt an das man Space drücken muss um das Spiel zu starten.

Alle Texte werden in schwarzer Farbe dargestellt und werden in der Bildschirmmitte angezeigt


Quellen:

Idee: Dominik Geller

Hilfe beim Coden: Adrian Pfeffer

Hauptakteure: Leon Geller, Carlos Kohl


Bedienungsanleitung:

Wenn man die level.txt Datei öffnet erkennt man mehrere Zeichen. Durch die Anderung dieser ändert sich auch das Level.

Dabeí steht der Buchstabe "G" für den Boden, "S" für die Stachel, "E" für die Ziellinie und "." für die Luft.

Wenn man die main.py Datei ausführt, wird das Spiel gestartet. Alle weiteren Infos sind im Spiel zu finden.
