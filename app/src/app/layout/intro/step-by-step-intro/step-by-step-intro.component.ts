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

import {Component, OnDestroy, OnInit} from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import {BehaviorSubject, Observable, Subscription, timer} from 'rxjs';
import {SpecialService} from '../../../framework/services/special.service';

@Component({
  selector: 'cmdb-step-by-step-intro',
  templateUrl: './step-by-step-intro.component.html',
  styleUrls: ['./step-by-step-intro.component.scss']
})
export class StepByStepIntroComponent implements OnInit, OnDestroy {

  private readonly STEPS = 'steps';
  private readonly EXECUTE = 'execute';

  public introInstance  = new BehaviorSubject<any[]>([]);
  private subscription: Subscription;
  private isReady: boolean = false;

  constructor(public activeModal: NgbActiveModal, private specialService: SpecialService) {}

  public ngOnInit(): void {
    this.subscription = timer(0, 1000).subscribe(result => {
      this.specialService.getIntroStarter().subscribe(value => {
        this.introInstance.next(value[this.STEPS]);
        this.isReady = value[this.EXECUTE];
      });
    });
  }

  public checkValid() {
    return this.isReady;
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }
}
