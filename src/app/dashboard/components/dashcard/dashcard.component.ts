import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'cmdb-dashcard',
  templateUrl: './dashcard.component.html',
  styleUrls: ['./dashcard.component.scss']
})
export class DashcardComponent {

  @Input() icon: string;
  @Input() name: string;
  @Input() numbers: number;

}
