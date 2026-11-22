import test from 'node:test';import assert from 'node:assert/strict';
import {bounds} from '../web/model.mjs';
test('no-delay intervals produce bounded quantiles and missing stays missing',()=>{assert.deepEqual(bounds([{lower:0,upper:5},{lower:10,upper:10},{lower:null,upper:null}]),{lower:5,upper:7.5,n:2});assert.deepEqual(bounds([]),{lower:null,upper:null,n:0});});
