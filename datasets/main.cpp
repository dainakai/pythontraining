#include<bits/stdc++.h>
#include<omp.h>
using namespace std;

const char* holograms_dir = "./holograms";
const char* data_dir = "./dat";
const char* fft_dir = "./fft";

const int itr = 100;
const int width = 512;
const int height = 512;
const int depth = 512;
const int dist = 1000;
const int num = 1000;
const double dx = 10.0;
const double diam = 80.0;
const double wave_len = 0.6328;
const int peak_bright = 127;
double re_prtcl_vol[depth][height][width];
double im_prtcl_vol[depth][height][width];
double x_prtcl[num];
double y_prtcl[num];
double z_prtcl[num];

char datname[100],holoname[100],fftname[100];

void trans_func (double re[height][width], double im[height][width], double posi_x);

FILE *fp;

int main(){
    srand((unsigned int)time(NULL));
    for (int index = 0; index < itr; index++){
        for (int n = 0; n < num; n++){
            x_prtcl[n] = rand() % width;
            y_prtcl[n] = rand() % height;
            z_prtcl[n] = rand() % depth;

            #pragma omp parallel for
            for (int i = 0; i < depth; i++){
                for (int j = 0; j < height; j++){
                    for (int k = 0; k < width; k++){
                        if ((double)((k-x_prtcl[i])*(k-x_prtcl[i]) + (j-y_prtcl[i])*(j-y_prtcl[i]) + (i-z_prtcl[i])*(i-z_prtcl[i])) > diam*diam/4.0){
                            re_prtcl_vol[i][j][k] = 1.0;
                        }
                    }
                }
            }
        }

        sprintf(datname,"%s/%05d.dat",data_dir,index);
        fp = fopen(datname,"w");
        for (int i = 0; i < depth; i++)
        {
            for (int j = 0; j < height; j++)
            {
                for (int k = 0; k < width; k++)
                {
                    fprintf(fp,"%.1lf ",re_prtcl_vol[i][j][k]);
                }
                fprintf(fp,"\n");
            }
            fprintf(fp,"\n\n");
        }
        fclose(fp);
    }
    
    return 0;
}

void trans_func (double re[height][width], double im[height][width], double posi_z){
    double tmp, C[3];
    C[0] = 2.0*M_PI*posi_z/wave_len;
    C[1] = wave_len*wave_len/height/height/dx/dx;
    C[2] = wave_len*wave_len/width/width/dx/dx;
    for (int i = 0; i < height; i++){
        for (int j = 0; j < width; j++){
            tmp = C[0]*sqrt(1.0 - C[1]*((double)i-height/2.0)*((double)i-height/2.0) - C[2]*((double)j-width/2.0)*((double)j-width/2.0));
            re[i][j] = cos(tmp);
            im[i][j] = sin(tmp);
        }
    }
}