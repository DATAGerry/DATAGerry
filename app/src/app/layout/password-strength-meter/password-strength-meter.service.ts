import { Injectable } from '@angular/core';

import * as zxcvbn_ from 'zxcvbn';

const zxcvbn = zxcvbn_;

@Injectable({
  providedIn: 'root'
})
export class PasswordStrengthMeterService {
  constructor() {
  }

  public score(password): number {
    const result = zxcvbn(password);
    return result.score;
  }

  public scoreWithFeedback(password): { score: number; feedback: { suggestions: string[]; warning: string } } {
    const result = zxcvbn(password);
    return {score: result.score, feedback: result.feedback};
  }
}
