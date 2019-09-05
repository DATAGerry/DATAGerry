import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { RenderResult } from '../../../models/cmdb-render';

@Component({
  selector: 'cmdb-object-footer',
  templateUrl: './object-footer.component.html',
  styleUrls: ['./object-footer.component.scss']
})
export class ObjectFooterComponent implements OnChanges{

  public objectID: number;
  private rr: RenderResult;

  @Input('renderResult')
  public set renderResult(rr) {
    if (rr !== undefined) {
      this.rr = rr;
      this.objectID = rr.object_information.object_id;
    }
  }

  public get renderResult() {
    return this.rr;
  }

  public ngOnChanges(changes: SimpleChanges): void {
    this.objectID = this.renderResult.object_information.object_id;
  }


}
