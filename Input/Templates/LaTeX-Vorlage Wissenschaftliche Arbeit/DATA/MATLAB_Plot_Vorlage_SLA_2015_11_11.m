%% Plot-Example Isonorm-Schrift
% Vorlage erstellt von: Johanna Schlupkothen
%                       Institut für Strukturmechanik und Leichtbau
%                       RWTH Aachen
%                       johanna.schlupkothen@sla.rwth-aachen.de
% Stand:                2015-Nov
% zur Anwendung in:     TeX-Vorlage für Studentische Arbeiten (SLA)
%**************************************************************************
%
% WICHTIG:              Vorher Isonorm3098 installieren
% Alternative Schrift:  IsonormD (Freeware download), dann die Bezeichnung
%                       im Skript ändern

% HINWEIS zur Einbindung in LaTeX:
%                       \begin{figure}
%                       \includegraphics[width=.96\textwidth]{Example_1.png}
%                       \caption{Beim Satz von 2 Plots auf einer A4-Seite
%                       ist immer noch Platz für eine zweizeilige
%                       Bildunterschrift}
%                       \label{fig:Example_1}
%                       \end{figure}
%                       Bei LaTeX Textbreite von 16cm und Texthöhe 22.5 cm
% *************************************************************************
% Allg. Hinweise:       Vermeiden von Farben, um Druckbarkeit in S/W zu
%                       gewährleisten
%                       Stattdessen mit unterschiedlichen Markern arbeiten
 set(0, 'DefaultTextInterpreter', 'none')
clear all, close all
plotprop        = {'PaperOrientation','portrait','WindowStyle','docked',...
                   'PaperPosition',[0,0,16,10],'PaperSize',[16,10],...
                   'PaperPositionMode','manual',...
                   'PaperUnits','centimeters','Color',[1,1,1]};    
%set Standard Schriftart
set(        0, 'FixedWidthFontName','Isonorm3098')
% Vorschlag zur Verwendung der Marker-Symbole in folgender Reihenfolge
Marksym         = {'s','d','v','^','>','<','o','*'};

it              = 1;
x_1             = 0:200:5000;
x_2             = 0:250:5000;
y_1             = 0.001*x_1.^2-2000;
y_2             = 1000*sin(x_2/1800*pi);
y_3             = 1000*cos(x_2/1800*pi)+1000;
fig_Example_2=figure(plotprop{:});
plot(x_1,y_1,'-sk','Linewidth',1,'MarkerfaceColor','k','Markersize',5), grid on, %grid minor
hold on
plot(x_2,y_2,'-dk','Linewidth',1,'MarkerfaceColor','k','Markersize',5)
plot(x_2,y_3,'-vk','Linewidth',1,'MarkerfaceColor','k','Markersize',5)
xlabel(gca,'X-Achsenbeschriftung [Einheit/Einheit]','Fontsize',9.5,'Fontname','Isonorm3098','FontWeight','normal'), 
ylabel(gca,'Y-Achsenbeschriftung [Einheit/Einheit]','Fontsize',9.5,'Fontname','Isonorm3098','FontWeight','normal')
% Schrift der Achsennummerierung anpassen und Rahmen anschalten (wird in
% der Regel automatisch entfernt, sobald die Achsengrenzen verschoben
% werden. Daher sollte unbedingt der nachfolgende Befehl zum Schluss
% ausgeführt werden)
set(gca,'Fontname','Isonorm3098','Fontsize',9.5,'Fontweight','normal','box','on')
legend('Parabelplot','Sinusplot','Cosinusplot','Location','Northwest')
set(legend,'box','on')
saveas(gcf,['Example_',num2str(it),'.fig']) 
print(gcf,'-dpng','-r300',['Example_',num2str(it)])
