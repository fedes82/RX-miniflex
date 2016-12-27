#include <mega16.h>
#include <stdio.h>  
#include <delay.h>
#include <string.h> 
#include <ctype.h>  

 // Constantes

#define xtal 3686400L // Frecuencia de cristal en [Hz] 
#define baud 9600     // define Baud rate
#define beep PORTD.3 
#define pulso PIND.7 
#define testpoint PORTD.4
 
// Prototipos de Funciones

void mide(void); 
void beeper(void); 
void configurar(void);


// global variables  

int conv; 
float Rx;
char caracter=0, temp = 0;
volatile unsigned char compareH=0, compareL=0; 
int i=0,nropulso = 0;;
//int cantidad;
//char buf[17];
volatile int Espero_300ms = 1, temptest =0;



//**************** INTERRUPCIONES  ************//

// Timer1 output compare A interrupt service routine
interrupt [TIM1_COMPA] void timer1_compa_isr(void)
{
// Place your code here
    Espero_300ms = 0;
  
  if (temptest )
  {temptest =0;
    testpoint =0;}
   else
   {temptest =1;
    testpoint =1;}
       
    TCNT1H=0x00;
    TCNT1L=0x00;  

}


//************** MAIN **************************/


void main(void)
{

    configurar();

while(1) //loop principal
{   inicio:
    caracter = getchar();
    switch (caracter)
    {
        case 'i':
        case 'I':
            // modo medicion, mide cada 300ms 49 veces 
            // (2grad/min => mide cada 0.01 grado) 
            // y espera el flanco ascendente en el pin
            // para volver a empezar y quedar sincronizado con el marker
            
            TCCR1B=0x00;    //el timer esta apagado
            TCNT1H=0x00;    // y el contador vale cero   
            TCNT1L=0x00;
            while (1)
            {
                nropulso = 0;
                Espero_300ms = 1;
                while(pulso == 1); //espera marker en bajo para empezar
                printf("mark\n");
                TCCR1B=0x0C;    //con esto enciendo el timer
                mide();            // 80 mseg
                //Rx=(float)conv*2560/1023;   
                nropulso++;
                //printf("%.2f\n",Rx); // 16.6 mseg en transmitir
                //printf("pulso nro %d\n", nropulso);
                printf("%d\n",conv);
                beeper();          // 100 mse                
                for ( i=49; i>0; i-- )
                {
                    while(Espero_300ms);    //el timer pone Espero_300ms = 0 en la interrupcion
                    Espero_300ms = 1;   //
                    mide();            // 80 mseg
                    //Rx=(float)conv*2560/1023; 
                    nropulso++;
                    //printf("%.2f\n",Rx); // 16.6 mseg en transmitir
                    printf("%d\n",conv);
                 //   printf("pulso nro %d\n", nropulso);
                    
                    beeper();          // 100 mse 
                    if (UCSRA & 0b10000000) //comprobar si hay un byte para leer en la uart
                    {
                        temp = getchar();
                        switch( temp) 
                        {
                            case 'T':   //condicion para terminar, recibir una 'T'
                                Espero_300ms = 1;
                                TCCR1B=0x00;    //con esto apago el timer
                                TCNT1H=0x00;    // y el contador vale cero   
                                TCNT1L=0x00;
                                beeper();          // 100 mse
                                beeper();          // 100 mse
                                beeper();          // 100 mse
                                goto inicio;
                                break;
                        
                            case 'U':   //aumento el delay entre mediciones
                                compareH += 1;
                                break;
                            case 'u':   //aumento el delay entre mediciones
                                compareL += 10;
                                break;
                            case 'L':   //disminuyo el delay entre mediciones
                                compareH -= 1 ;
                                break;
                            case 'l':   //disminuyo el delay entre mediciones
                                compareL -=10 ;
                                break;
                            default:
                                break;
                        }
                        OCR1AH = compareH;
                        OCR1AL = compareL;
                        printf("OCR1AH vale, %x\n", OCR1AH);
                        printf("OCR1AL vale %x\n", OCR1AL);
                        
                    }
                }
                Espero_300ms = 1;
                TCCR1B=0x00;    //con esto apago el timer
                TCNT1H=0x00;    // y el contador vale cero   
                TCNT1L=0x00;
                
            }
            break;
        case 'p':
        case 'P':
            // Prueba de comunicacion
            printf("COM OK \n");
            beeper();          // 100 mse
            break;
        default:
            putchar(caracter);
            break;

    }
    
}// fin loop principal
}

    /*
    while(pulso == 1);      // espera pulso  y manda primer medida
    mide();            // 80 mseg
    Rx=(float)conv*2560/1023;   
    printf("%.2f",Rx); // 16.6 mseg en transmitir
    beeper();          // 100 mseg 
     
    while(1)
    { 
        switch(getchar())// espera que llegue la orden de medor
        {
            case '1':mide();            // 80 mseg
                  Rx=(float)conv*2560/1023;   
                  printf("%.2f",Rx); // 16.6 mseg en transmitir
                  beeper();          // 100 mseg 
                  break;             // 
            case 'T':goto inicio; 
            case 'P':printf("comunicacion ON /n");
                  break;
        }  
    }
}
*/

/*************************************************
                    FUNCIONES
**************************************************/                  


/*------------------ FUNCION CONFIGURAR ----------------*/

void configurar(void)
{
     MCUCR=0X00;      // asegura no memoria externa
     
     DDRA=0X00;       //Puera A entradas analogicas
     PORTA=0XF0;      //habilita pull-up MSB
     
     DDRB=0XFF;       // LSB salidas = control display
     PORTB=0XFF;      // MSB salidas = SPI y RAM
     
     DDRC=0b00000000; // LSB entradas = Teclado
     PORTC=0xFF;      // 1/2 MSB entradas =llsve y seguro
     
     DDRD=0x1F;       // LSB RS232, interrup y chirrara y testpoint
     PORTD=0xFF;      // MSB entradas con Pull- UP
     
      
      /*----------- inicializa Puerta serie ----------- */
        
     UCSRA=0x00;   //  4800 Baudios  8 Data, 1 Stop, No Parity
     UCSRB=0x18;   //  Rx On ; Tx On
     UCSRC=0x86;   //  USART modo asincronico
     UBRRH=0x00;
     UBRRL=xtal/16/baud-1;  //4800
     //UBRRL=0x17;        //0x17 => 9600  
     
     /*---------- Inicializa ADC ------------------*/ 
     
     ADCSRA=0x86;     // ADC Clock frequencia: 57.656 kHz
                      // sin interrupcion
     ADMUX=0b11000000;// Selecciona input simple en canal 0
                      // y referencia interna=2,56V

     /*-------------- Inicializa Timer1 ---------------*/
    // Timer/Counter 1 initialization
    // Clock source: System Clock
    // Clock value: 31,250 kHz
    // Mode: CTC top=OCR1A
    // OC1A output: Discon.
    // OC1B output: Discon.
    // Noise Canceler: Off
    // Input Capture on Falling Edge
    // Timer1 Overflow Interrupt: Off
    // Input Capture Interrupt: Off
    // Compare A Match Interrupt: On
    // Compare B Match Interrupt: Off
    
    
    TCCR1A=0x00;
    TCCR1B=0x0C;
    TCNT1H=0x00;
    TCNT1L=0x00;
    ICR1H=0x00;
    ICR1L=0x00;              
    //compareH = 0x21;   
    //compareL =0xAD;
    compareH = 0x10;   
    compareL =0xD6;
    OCR1AH=compareH;
    OCR1AL=compareL;
    OCR1BH=0x00;
    OCR1BL=0x00;
    
    /*inicializacion de interrupciones del timer*/
    TIMSK=0x10;
    
    //habilito globalmente las interruciones
    #asm("sei")
                      
}

/*--------------- FUNCION BEEPER ------------------------------------*/

 void beeper(void)  
  {
    beep = 0;
    delay_ms(50); 
    if(conv < 799) beep = 1; // si es manor a 2v = 799 cuentas apaga 
    //delay_ms(150);
  }

 /*------------------ FUNCION MIDE ----------------*/

 
void mide(void)
{                     
 // mide      
  ADMUX=0b11000000;   // entrada simple canal 0
  delay_ms(70);      // y referencia interna = 2,56V
  ADCSRA|=0x40;       // Arranca conversor AD
  delay_ms(10);
  conv=ADCW & 0x03FF; // adquiere el dato en 10 bits
                      // 2560 mV = 1024 cuentas = 2.56 volts => 
  //conv=0x03ff;        // esto para probar
}                
