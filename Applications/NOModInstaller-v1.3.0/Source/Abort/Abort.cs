﻿using System;
using System.Windows.Forms;

namespace NOModInstaller {
	public partial class Abort : Form {
		public Abort () {
			InitializeComponent();
		}

		private void CloseButton_Click (object sender, EventArgs e) {
			Close();
		}
	}
}
