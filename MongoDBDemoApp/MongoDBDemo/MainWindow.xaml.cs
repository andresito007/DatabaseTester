using System.Collections.Generic;
using System.Windows;
using MongoDataAccess.DataAcess;
using MongoDataAccess.Models;

namespace MongoDBDemo
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        ChoreDataAccess db = new ChoreDataAccess();

        private async void btnInsert_Click(object sender, RoutedEventArgs e)
        {
            await db.CreateUser(new UserModel() { FirstName = "Andres", LastName = "Gaona", data = new List<double>() { 0, 0.1, 0.2, 0.3 } });
        }

        private async void btGetUsers_Click(object sender, RoutedEventArgs e)
        {
            List<UserModel> users = await db.GetAllUsers();
            ChoreModel chore = new ChoreModel() { AssignedTo = users[0], ChoreText = "Mow the lawn", FrequencyInDays = 7 };
            await db.CreateChore(chore);
        }
    }
}
