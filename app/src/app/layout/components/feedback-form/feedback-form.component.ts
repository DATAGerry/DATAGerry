import { Component, OnInit } from '@angular/core';
import {SystemService} from "../../../settings/system/system.service";

@Component({
  selector: 'cmdb-feedback-form',
  templateUrl: './feedback-form.component.html',
  styleUrls: ['./feedback-form.component.scss']
})
export class FeedbackFormComponent implements OnInit {

  public systemInfo: any[] = [];

  constructor(private systemService: SystemService) { }

  ngOnInit() {
    this.systemService.getDatagerryInformation().subscribe((infos: any[]) => {
      this.systemInfo = infos;
    });
  }

}
