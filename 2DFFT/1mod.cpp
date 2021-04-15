/******************************************************************************
PROGRAM NAME : Digital holography generating
AUTHER : Dai Nakai
DATE : 2021/4/13
******************************************************************************/
#include<bits/stdc++.h>
using namespace std;

const char* refimg = "./512.bmp";
const char* image = "./outputimage.bmp";
const char* hologram = "./outputholography.bmp";
char* header_buf[1078];

const int height = 512;
const int width = 512;
const double dx = 10.0;
const double diam = 80.0;
const double posi_x = 2560.0;
const double posi_y = 2560.0;
const double posi_z = 15000.0;
const double wave_length = 0.6328;

void S_fft (double *ak, double *bk, int N, int ff);
void twoDimFFT(double re[height][width], double im[height][width], int flag);

unsigned char image_out[height][width];
double re_object[height][width];
double im_object[height][width];
double re_trans[height][width];
double im_trans[height][width];
double re_holography[height][width];
double im_holography[height][width];


FILE *fp;
/*********************************main****************************************/
int main () {
    if(!(fp = fopen(refimg,"rb"))){
        printf("No reference image. quitting...\n");
        exit(1);
    }
    fread(header_buf,sizeof(unsigned char),1078,fp);
    fclose(fp);

    double C[2], temp;
    C[0] = wave_length*wave_length/height/height/dx/dx;
    C[1] = wave_length*wave_length/width/width/dx/dx;
    for (int i = 0; i < height; i++){
        for (int j = 0; j < width; j++){
            if(((double)j*dx - posi_x)*((double)j*dx - posi_x) + ((double)i*dx - posi_y)*((double)i*dx - posi_y) > diam*diam/4.0){
                re_object[i][j] = 127.0;
            }else{
                re_object[i][j] = 0.0;
            }
            im_object[i][j] = 0.0;
            image_out[i][j] = (unsigned char)re_object[i][j];

            temp = 2.0*M_PI*posi_z/wave_length*sqrt(1.0-C[0]*((double)i - height/2.0)*((double)i - height/2.0)-C[1]*((double)j - width/2.0)*((double)j - width/2.0));
            re_trans[i][j] = cos(temp);
            im_trans[i][j] = sin(temp);
        }
    }

    fp = fopen(image,"wb");
    fwrite(header_buf,sizeof(unsigned char),1078,fp);
    fwrite(image_out,sizeof(unsigned char),width*height,fp);
    fclose(fp);

    twoDimFFT(re_object,im_object,1);

    for (int i = 0; i < height; i++){
        for (int j = 0; j < width; j++){
            re_holography[i][j] = re_object[i][j]*re_trans[i][j] - im_object[i][j]*im_trans[i][j];
            im_holography[i][j] = re_object[i][j]*im_trans[i][j] + im_object[i][j]*re_trans[i][j];
        }
    }
    
    twoDimFFT(re_holography,im_holography,-1);

    for (int i = 0; i < height; i++){
        for (int j = 0; j < width; j++){
            image_out[i][j] = (unsigned char)sqrt(re_holography[i][j]*re_holography[i][j] + im_holography[i][j]*im_holography[i][j]);
        }
    }

    fp = fopen(hologram,"wb");
    fwrite(header_buf,sizeof(unsigned char),1078,fp);
    fwrite(image_out,sizeof(unsigned char),width*height,fp);
    fclose(fp);

    return 0;
    
}

void twoDimFFT(double re[height][width], double im[height][width], int flag){
    double re_temp1[width], im_temp1[width], re_temp2[height], im_temp2[height];

    if((flag != 1) && (flag != -1)){
        printf("flag of FFT must be either 1 or -1. Software quitting... \n");
        exit(1);
    }

    if(flag == -1){
        double re_array[height][width], im_array[height][width];
        for (int i = 0; i < height/2; i++){
            for (int j = 0; j < width/2; j++){
                re_array[i][j] = re[i + height/2][j + width/2];
                im_array[i][j] = im[i + height/2][j + width/2];
                re[i + height/2][j + width/2] = re[i][j];
                im[i + height/2][j + width/2] = im[i][j];
                re[i][j] = re_array[i][j];
                im[i][j] = im_array[i][j];
            }
        }

        for (int i = height/2; i < height; i++)
        {
            for (int j = 0; j < width/2; j++)
            {
                re_array[i][j] = re[i - height/2][j + width/2];
                im_array[i][j] = im[i - height/2][j + width/2];
                re[i - height/2][j + width/2] = re[i][j];
                im[i - height/2][j + width/2] = im[i][j];
                re[i][j] = re_array[i][j];
                im[i][j] = im_array[i][j];
            }
        }
    }

    for (int i = 0; i < height; i++){
        for (int j = 0; j < width; j++){
            re_temp1[j] = re[i][j];
            im_temp1[j] = im[i][j];
        }
        S_fft(re_temp1,im_temp1,width,flag);
        for (int j = 0; j < width; j++){
            re[i][j] = re_temp1[j];
            im[i][j] = im_temp1[j];
        }
    }

    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            re_temp2[j] = re[j][i];
            im_temp2[j] = im[j][i];
        }
        S_fft(re_temp2,im_temp2,height,flag);
        for (int j = 0; j < height; j++)
        {
            re[j][i] = re_temp2[j];
            im[j][i] = im_temp2[j];
        }
    }

    if(flag == 1){
        double re_array[height][width], im_array[height][width];
        for (int i = 0; i < height/2; i++){
            for (int j = 0; j < width/2; j++){
                re_array[i][j] = re[i + height/2][j + width/2];
                im_array[i][j] = im[i + height/2][j + width/2];
                re[i + height/2][j + width/2] = re[i][j];
                im[i + height/2][j + width/2] = im[i][j];
                re[i][j] = re_array[i][j];
                im[i][j] = im_array[i][j];
            }
        }

        for (int i = height/2; i < height; i++)
        {
            for (int j = 0; j < width/2; j++)
            {
                re_array[i][j] = re[i - height/2][j + width/2];
                im_array[i][j] = im[i - height/2][j + width/2];
                re[i - height/2][j + width/2] = re[i][j];
                im[i - height/2][j + width/2] = im[i][j];
                re[i][j] = re_array[i][j];
                im[i][j] = im_array[i][j];
            }
        }
    }
}

void S_fft(double *ak, double *bk, int N, int ff){
    int i,j,k,k1,num,nhalf,phi,phi0,rot[N];
    double s,sc,c,a0,b0,tmp;

    for (i = 0; i < N; i++){
        rot[i] = 0;
    }

    nhalf = N/2;
    num = N/2;
    sc = 2.0*M_PI/(double)N;

    while(num>=1){
        for (j = 0; j < N; j+=(2*num)){
            phi = rot[j]/2;
            phi0 = phi + nhalf;
            c = cos(sc*(double)phi);
            s = sin(sc*(double)(phi*ff));

            for(k=j; k<j+num; k++){
                k1 = k+num;
                a0 = ak[k1]*c - bk[k1]*s;
                b0 = ak[k1]*s + bk[k1]*c;
                ak[k1] = ak[k]-a0;
                bk[k1] = bk[k]-b0;
                ak[k] +=a0;
                bk[k] += b0;
                rot[k] = phi;
                rot[k1] = phi0;
            }
        }
        num /= 2;
    }

    if(ff<0){
        for ( i = 0; i < N; i++){
            ak[i] /= (double)N;
            bk[i] /= (double)N;
        }
    }

    for(i=0; i<N-1; i++){
        if((j=rot[i])>i){
            tmp=ak[i]; ak[i] = ak[j]; ak[j]=tmp;
            tmp=bk[i]; bk[i] = bk[j]; bk[j]=tmp;
        }
    }
}
