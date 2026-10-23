#                                                                                                   
#    	G N U P L O T                                                                                 
#    	version 5.2                                                              
#    	                                
#       SLA template x-y-plots
#
# 
# lt=line_type, lw=line_width, ls=line_style
#                               
#
############# EPS file output #############
#set fontpath 'C:\Windows\Fonts\Isonorm3098'
#set term postscript eps enhanced monochrome lw 1 font "Isonorm3098,22" 
#set term postscript eps enhanced color lw 1 font "Isonorm3098,22"
#
#set output "eps/Gnuplot_Demo.eps" 
set term pngcairo size 1024,768 font "Isonorm3098,12" 													# choose either eps or png, does not work when both are active
set output "eps/Gnuplot_Demo.png" 
show output  
#                                                                  
### set data types ###                                          
set xdata                                                                                           
set ydata                                                                                           
#
############# initialization #############
set nolabel                                                                                         
set noarrow                                                                                                                                                             
set nologscale                                                                                      
set nopolar                                                                                         
set noparametric                                                                                    
set nocontour
set encoding default  
#
############# define diagram frame #############                                               
#set title ""                                    
set border 31 lt -1 lw 0.992    						# default setting is 31                                                                   
set size ratio 0.71										# ratio of the y-axis length tothe x-axis length                                                                       
#
############# axis settings #############
set tics in                     						# tic marks to be drawn inwards                                                                                                                                                
set mxtics default              						# minor tic marks along the x axis                                                                     
set mytics default              						# minor tic marks along the y axis                                                                                                                                        
set xtics border mirror norotate autofreq     			# mirror: put unlabeled tics at the same positions on the opposite border                                                      
set ytics border mirror norotate autofreq                                                                                                      
#
############# grid settings #############
set grid lt 0 lw 0.709                                         
#                                                                                                   
############# set names of dummy variables #############                                         
set dummy x,y                                                                                       
#                                                                                                   
############# set variables to standard format ##############                                                       
set format x "%g"                                       # exponential notation; an "e" or "E" before the power & floating point notation                                            
set format y "%g"                                                                                                                                                                      
#                                                                                                   
############# no lines outside the graph #############
set noclip points                                       # draw data points whith center inside the plot boundaries, whose point symbol extends past a boundary line                                            
set clip one                                            # draw the in-range portion of line segments with one endpoint out of range                                         
set noclip two                                          # do not draw the in-range portion of linesegments with both endpoints out of range                                            
#
############# set legend #############                                            
#set key title "legend"                                 														# define the legend title                                           
set key top left Left opaque noreverse box linetype -2 linewidth 1.417 samplen 4 spacing 1.1 width -2   		# Justification of the plot titles within the key is controlled by Left or Right
#unset key                                              														# deactivate legend                                 
#
############# graph settings #############                                        
set pointsize 1                                         # scales the size of the points used in plots                                                                                     
set mapping cartesian                                   # {cartesian | spherical | cylindrical}                                                                                                                       
#
set style data points                                   # changes the default plotting style for data plots to points                                             
set style function lines                                # changes the default plotting style for function plots to lines                                           

############# define line styles #############			# Each terminal has a default set of line and point types, which can be viewed by using the command "test" in the gnuplot console
set colorsequence default
set style line 1 lt 8 lw 2 dt 4 pt 1 pn 10
set style line 2 lt 7 lw 1 pt 5 pn 10
set style line 3 lt 6 lw 1 pt 8 pn 10
set style line 4 lt 4 lw 1 pt 7 pn 10
set style line 5 lt 3 lw 1 pt 3 pn 10
set style line 6 lt 2 lw 1 pt 1 pn 10
set style line 7 lt 1 lw 1 pt 2 pn 10
set colorsequence podo
set style line 8 lt 8 lw 1 dt 2 pt 5 pn 10
set style line 9 lt 7 lw 1 dt 2 pt 8 pn 10
set colorsequence classic
set style line 10 lt 5 lw 1 dt 2 pt 7 pn 10
set style line 11 lt 4 lw 1 dt 2 pt 3 pn 10
set style line 12 lt 3 lw 1 dt 2 pt 1 pn 10
set style line 13 lt 2 lw 1 dt 2 pt 2 pn 10
set style line 14 lt 9 lw 1 dt 2 pt 4 pn 10
set style line 15 lt 8 lw 1 pt 9 pn 10
set style line 16 lt 9 lw 1 pt 6 pn 10
set style line 17 lt -1 lw 1 pt 11 pn 10

#
############# insert arbitrary lable #############
#set label "{/Symbol D}T=-500{/Symbol \260}C: q_{crit}=470.5 N/mm;" at 14,575
set label "P_{crit}=28.2 kN" at 1.2,31.5
#set arrow 1 from 26,500 to 28.17,470.512 head filled lw 1
set arrow 2 from 0,28.17 to 1.5,28.17 nohead lw 1 dt 2
#set arrow 3 from 0,470.512 to 30,470.512 nohead lw 1 dt 2
#
#set label "{/Symbol D}T=   0{/Symbol \260}C: q_{crit}=276.2 N/mm;" at 14,205
#set label "v_{crit}=16.4 mm" at 22.5,155
#set arrow 4 from 20,230 to 16.36,276.156 head filled lw 1
#set arrow 5 from 16.36,0 to 16.36,300 nohead lw 1 dt 2
#set arrow 6 from 0,276.156 to 18,276.156 nohead lw 1 dt 2
#
#set label "{/Symbol D}T= 200{/Symbol \260}C: q_{crit}=129.4 N/mm;" at 14,80
#set label "v_{crit}=7.6 mm" at 22.5,30
#set arrow 7 from 13.6,55 to 7.63,129.414 head filled lw 1
#set arrow 8 from 7.63,0 to 7.63,150 nohead lw 1 dt 2
#set arrow 9 from 0,129.414 to 9,129.414 nohead lw 1 dt 2
#
############# define angle unit #############
set angles radians                                                                                  
#


############################################################################################################################################
#plot###plot###plot###plot###plot###plot###plot###plot###plot###plot###plot###plot###plot###plot###plot###plot###plot###plot###plot###plot##
############################################################################################################################################
set encoding iso_8859_1																																# selects a character encoding
set xrange [ 0 : 1.5 ] noreverse nowriteback  
set xlabel "Weg [mm]"  

set yrange [ 0: 100 ] noreverse nowriteback  
set ylabel 'Kraft [kN]'  #offset -1,0,0


#---------------------
set datafile separator ";"
plot	sin(10*x)+10  title 'sin(10x)+10'  ls 2  with linespoints ,\
40*x title '40x'  ls 1  with linespoints ,\
12.5* sin(10*x)+10 title '12.5*sin(10x)+10'  ls 8  with linespoints ,\
"data/DemoCSV.csv"  using ($1):($2/1000)  title 'Test-Data'  ls 3  with linespoints ,\
"data/DemoRPT.rpt"  using (-$4):(-$2/1000)  title 'FE-Data'  ls 4  with linespoints ,\

############################################################################################################################################

replot

pause -1 "press key to continue"
