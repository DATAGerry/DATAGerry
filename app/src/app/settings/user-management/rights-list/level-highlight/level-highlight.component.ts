import { Component, HostBinding, Input, OnInit } from '@angular/core';
import { Right } from '../../../../management/models/right';

@Component({
  // tslint:disable-next-line:component-selector
  selector: '[cmdb-level-highlight]',
  templateUrl: './level-highlight.component.html',
  styleUrls: ['./level-highlight.component.scss']
})
export class LevelHighlightComponent implements OnInit {

  @HostBinding('class') public backgroundClass;
  @Input() public level: number;
  @Input() public rightLevels: { [key: number]: string };
  public levelName: string;

  public ngOnInit(): void {
    this.levelName = this.getLevelName(this.level);
    switch (this.level) {
      // NOSET
      case 0: {
        this.backgroundClass = null;
        break;
      }
      // PERMISSION
      case 10: {
        this.backgroundClass = null;
        break;
      }
      // PROTECTED
      case 30: {
        this.backgroundClass = 'bg-secondary';
        break;
      }
      // SECURE
      case 50: {
        this.backgroundClass = 'bg-info';
        break;
      }
      // DANGER
      case 80: {
        this.backgroundClass = 'bg-warning';
        break;
      }
      // CRITICAL
      case 100: {
        this.backgroundClass = 'bg-danger';
        break;
      }
      default: {
        this.backgroundClass = null;
        break;
      }
    }
  }


  public getLevelName(idx: number): string {
    try {
      if (this.rightLevels[idx] !== undefined) {
        return this.rightLevels[idx];
      } else {
        return null;
      }
    } catch (e) {
      return null;
    }

  }

}
