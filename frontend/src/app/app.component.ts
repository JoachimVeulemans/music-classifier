import { Component } from '@angular/core';
import { ApiService } from './api.service';
import { SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
    predictions: number[] = [];
    filename = '';
    filedata: SafeResourceUrl = '';
    selectedFile: File;
    uploadURL = '';

    public doughnutChartLabels = ['trumpet', 'grand piano', 'saxophone', 'guitar', 'clarinet', 'drums'];
    public doughnutChartData = [0, 0, 0, 0, 0, 0];
    public doughnutChartType = 'doughnut';
    public doughnutChartOptions = {
        responsive: true
      };

    constructor(private apiService: ApiService) { }

    upload(): void {
        this.apiService.upload(this.selectedFile).subscribe((value) => {
            this.predictions = value;
            this.doughnutChartData = [];
            this.doughnutChartLabels = [];
            value.predictions.forEach(prediction => {
                this.doughnutChartData.push(prediction[1]);
                this.doughnutChartLabels.push(prediction[0]);
            });
        }, (error) => {
            console.log('====================================');
            console.log(error.message);
            console.log('====================================');
        });
    }

    classifyUrl(): void {
        this.apiService.classifyUrl(this.uploadURL).subscribe((value) => {
            this.predictions = value;
            this.predictions = value;
            this.doughnutChartData = [];
            this.doughnutChartLabels = [];
            value.predictions.forEach(prediction => {
                this.doughnutChartData.push(prediction[1]);
                this.doughnutChartLabels.push(prediction[0]);
            });
        }, (error) => {
            console.log('====================================');
            console.log(error.message);
            console.log('====================================');
        });
    }

    handleFileInput(files: FileList): void {
        this.uploadURL = '';
        this.selectedFile = files[0];

        const reader = new FileReader();

        reader.addEventListener('load', () => {
          (document.getElementById('uploadImagePreview') as HTMLImageElement).src = reader.result.toString();
        }, false);

        if (this.selectedFile) {
          reader.readAsDataURL(this.selectedFile);
        }
    }
}
