import { Component, OnInit } from '@angular/core';
import { StatusService } from '../services/status.service';

@Component({
  selector: 'cmdb-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.scss'],
  providers: [StatusService]
})
export class StatusComponent implements OnInit {

  constructor(private statusService: StatusService) {
  }

  public ngOnInit(): void {
  }

}
