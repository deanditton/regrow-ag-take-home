# Solution

### Code Style:
The code style is intended to mimic provided example as closely as practical.

### Users:
Users will have multiple fields(Pastures). Farmers do not tend to have only a single Field in a farm. 
Future/Practical considerations Fields would probably have a "Farm" concept as their root table this step was omitted 
due to brevity of the solution. 

### Data Design
The Pasture 1 -> m PastureRecord table structure was used to cover the caveats in the requirements for flexible
and unknown future data need. 

By having a Pasture table you can encode your required information / Metadata about a Field and this data can be 
considered more static than the Record table data. This table should be dense. 

The Record table is allowed to be sparse it offers flexibility for future.

In the case of Years and Seasons the Record table allows for multiple rows to be linked to the same year / pasture  combination. 
Reason if a farmer has a split crop / tillage depth on a pasture you want to store that information then reconcile it later. 

In a practical use case the next step for this pattern would be a reconciliation table and/or view as a support structure
for easier querying. The advantage of materialised views is that if a pattern of data becomes common for a set of users
i.e American Farmers maintaining a reconciled "view" would allow for changing data gathering of this group without 
changing underlying data representation.

Pattern will work well in a data lake / warehouse environment.

Those types of considerations must be driven by usage and are far beyond the scope for build out of this exercise.




