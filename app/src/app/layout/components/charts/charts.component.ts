/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import {Component, Input, AfterViewInit, AfterViewChecked, ViewChild } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
// IMPORTANT
// chartjs-plugin-datalabel must be loaded after the Chart.js library!
import { Chart } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';

@Component({
  selector: 'cmdb-charts',
  templateUrl: './charts.component.html',
  styleUrls: ['./charts.component.scss']
})
export class ChartsComponent implements AfterViewInit, AfterViewChecked {

  @ViewChild('chartcanvas', {static : false})
  public chartRef;

  @Input() chartType: string;
  @Input() labelColors: any[];
  @Input() chartOptions: {};
  private chart;

  private labels = new BehaviorSubject<any[]>([]);
  @Input() set dataLabels(value: string[]) {
    this.labels.next(value);
  }

  get dataLabels() {
    return this.labels.getValue();
  }

  private items = new BehaviorSubject<any[]>([]);
  @Input() set dataItems(value: any[]) {
    this.items.next(value);
  }

  get dataItems() {
    return this.items.getValue();
  }

  ngAfterViewInit() {
    this.chart = new Chart(this.chartRef.nativeElement, {
      plugins: [ChartDataLabels],
      type: this.chartType,
      data: {
        datasets: [{
          backgroundColor: this.labelColors,
          datalabels: {
            color: '#FFF', font: { size: 12 }
          }
        }]
      },
    });
    this.chart.data.labels = this.dataLabels;
    this.chart.data.datasets[0].data = this.dataItems;
    this.chart.options = this.chartOptions;
    this.chart.update(true);
  }

  ngAfterViewChecked() {
    this.chart.update(true);
  }
}
